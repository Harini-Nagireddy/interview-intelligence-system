from modules.video_analysis import analyze_video
from modules.audio_analysis import analyze_audio
from modules.speech_analysis import analyze_speech
from modules.scoring import (
    score_camera_presence,
    score_voice,
    score_communication,
    final_interview_score
)
from modules.merge_media import merge_audio_video
from modules.report_generator import generate_report


def run_full_interview_analysis(candidate, topic):
    raw_video = "recordings/mock_interview.mp4"
    raw_audio = "recordings/mock_interview.wav"
    final_video = "recordings/final_interview.mp4"

    # Merge media
    merge_audio_video(raw_video, raw_audio, final_video)

    # VIDEO analysis
    video_result = analyze_video(final_video)
    camera_presence = video_result["camera_presence"]

    # AUDIO analysis
    audio_result = analyze_audio(final_video)
    speech_ratio = audio_result["speech_duration_sec"] / audio_result["total_audio_duration_sec"]
    speech_pace = audio_result["speech_pace"]

    # SPEECH / NLP
    speech_result = analyze_speech("temp_audio.wav")
    word_count = speech_result["word_count"]
    filler_words = speech_result["filler_words_count"]
    structure = speech_result["speech_structure"]

    # SCORING
    cam_score, cam_label = score_camera_presence(camera_presence)
    voice_score, voice_label = score_voice(speech_ratio, speech_pace)
    comm_score, comm_label = score_communication(word_count, filler_words, structure)

    final_score, final_label = final_interview_score(
        cam_score, voice_score, comm_score
    )

    results = {
        "Camera Presence": (cam_score, cam_label),
        "Voice & Pace": (voice_score, voice_label),
        "Communication": (comm_score, comm_label),
        "Final Interview Score": (final_score, final_label)
    }

    # PDF REPORT
    report_path = generate_report(candidate, topic, results)

    return results, report_path
