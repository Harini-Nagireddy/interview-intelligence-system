import cv2
import time
import os
import sounddevice as sd
from scipy.io.wavfile import write
import threading

QUESTIONS = [
    "Tell me about yourself",
    "Explain one project you worked on",
    "What are your strengths?",
    "Describe a challenge you faced"
]

def record_audio(duration, audio_path, fs=44100):
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(audio_path, fs, recording)

def start_live_interview(output_path="recordings/mock_interview.mp4"):
    os.makedirs("recordings", exist_ok=True)

    video_path = output_path
    audio_path = "recordings/mock_interview.wav"

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not accessible")
        return None

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(
        video_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        20.0,
        (width, height)
    )

    total_duration = len(QUESTIONS) * 15

    # Start audio recording in background
    audio_thread = threading.Thread(
        target=record_audio,
        args=(total_duration, audio_path)
    )
    audio_thread.start()

    cv2.namedWindow("Mock Interview", cv2.WINDOW_NORMAL)

    for question in QUESTIONS:
        start_time = time.time()
        while time.time() - start_time < 15:
            ret, frame = cap.read()
            if not ret:
                break

            remaining = 15 - int(time.time() - start_time)

            cv2.rectangle(frame, (0, 0), (width, 120), (0, 0, 0), -1)
            cv2.putText(frame, f"Q: {question}", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, f"Time left: {remaining}s", (20, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            out.write(frame)
            cv2.imshow("Mock Interview", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    audio_thread.join()

    return video_path, audio_path
