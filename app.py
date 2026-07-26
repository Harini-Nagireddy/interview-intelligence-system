from flask import Flask, render_template, request, jsonify, send_file, session
import os
import uuid
import json
import base64
from datetime import datetime
from modules.question_bank import get_questions_for_role, AVAILABLE_ROLES
from modules.audio_analysis import analyze_audio
from modules.video_analysis import analyze_video_frames
from modules.speech_analysis import analyze_speech
from modules.scoring import calculate_scores
from modules.report_generator import generate_pdf_report

app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = "uploads"
REPORTS_FOLDER = "reports"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html", roles=AVAILABLE_ROLES)


@app.route("/interview")
def interview():
    role = request.args.get("role", "Software Engineer")
    candidate_name = request.args.get("name", "Candidate")
    session_id = str(uuid.uuid4())[:8]
    questions = get_questions_for_role(role)
    return render_template(
        "interview.html",
        role=role,
        candidate_name=candidate_name,
        questions=json.dumps(questions),
        session_id=session_id,
    )


@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        session_id = data.get("session_id", str(uuid.uuid4())[:8])
        candidate_name = data.get("candidate_name", "Candidate")
        role = data.get("role", "Software Engineer")
        responses = data.get("responses", [])  # list of {question, answer, duration, video_frames, audio_data}

        all_results = []
        for i, resp in enumerate(responses):
            question = resp.get("question", "")
            answer_text = resp.get("answer_text", "")
            duration = resp.get("duration", 60)
            video_frames_b64 = resp.get("video_frames", [])
            audio_data_b64 = resp.get("audio_data", "")
            silence_ratio = resp.get("silence_ratio", 0.3)
            filler_count = resp.get("filler_count", 0)
            word_count = resp.get("word_count", 0)

            # Video analysis
            video_metrics = analyze_video_frames(video_frames_b64)

            # Audio analysis (from client-side metrics passed)
            audio_metrics = {
                "speech_duration": duration * (1 - silence_ratio),
                "silence_duration": duration * silence_ratio,
                "silence_ratio": silence_ratio,
                "speech_rate": word_count / max(duration / 60, 0.1),
            }

            # Speech/NLP analysis
            speech_metrics = analyze_speech(answer_text, filler_count, word_count)

            # Scoring
            scores = calculate_scores(video_metrics, audio_metrics, speech_metrics)

            all_results.append(
                {
                    "question": question,
                    "answer": answer_text,
                    "duration": duration,
                    "video_metrics": video_metrics,
                    "audio_metrics": audio_metrics,
                    "speech_metrics": speech_metrics,
                    "scores": scores,
                }
            )

        # Generate overall scores
        overall = {
            "confidence": round(sum(r["scores"]["confidence"] for r in all_results) / max(len(all_results), 1), 1),
            "communication": round(sum(r["scores"]["communication"] for r in all_results) / max(len(all_results), 1), 1),
            "engagement": round(sum(r["scores"]["engagement"] for r in all_results) / max(len(all_results), 1), 1),
            "fluency": round(sum(r["scores"]["fluency"] for r in all_results) / max(len(all_results), 1), 1),
            "content": round(sum(r["scores"]["content"] for r in all_results) / max(len(all_results), 1), 1),
        }
        overall["total"] = round(sum(overall.values()) / len(overall), 1)

        # Generate PDF report
        report_filename = f"report_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        report_path = os.path.join(REPORTS_FOLDER, report_filename)
        generate_pdf_report(
            report_path,
            candidate_name=candidate_name,
            role=role,
            session_id=session_id,
            results=all_results,
            overall=overall,
        )

        return jsonify(
            {
                "success": True,
                "session_id": session_id,
                "overall": overall,
                "results": all_results,
                "report_url": f"/download_report/{report_filename}",
            }
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/report/<session_id>")
def report(session_id):
    return render_template("report.html")


@app.route("/download_report/<filename>")
def download_report(filename):
    path = os.path.join(REPORTS_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name=filename)
    return "Report not found", 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
