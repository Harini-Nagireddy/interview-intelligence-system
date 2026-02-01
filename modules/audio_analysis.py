import wave
import contextlib
import numpy as np
from moviepy import VideoFileClip

def analyze_audio(video_path):
    audio_path = "temp_audio.wav"

    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, logger=None)

    with contextlib.closing(wave.open(audio_path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)

    audio = wave.open(audio_path, 'rb')
    signal = audio.readframes(-1)
    signal = np.frombuffer(signal, dtype=np.int16)

    threshold = 500
    voiced = np.sum(np.abs(signal) > threshold)
    total = len(signal)

    speech_ratio = voiced / total
    speech_time = duration * speech_ratio
    silence_time = duration - speech_time

    if speech_ratio > 0.6:
        pace = "Fast"
    elif speech_ratio > 0.4:
        pace = "Normal"
    else:
        pace = "Slow"

    return {
        "total_audio_duration_sec": round(duration, 2),
        "speech_duration_sec": round(speech_time, 2),
        "silence_duration_sec": round(silence_time, 2),
        "speech_pace": pace
    }
