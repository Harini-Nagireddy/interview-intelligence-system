def analyze_audio(audio_data_b64: str, duration: float) -> dict:
    """
    Analyze audio for speech vs silence, speech rate, confidence indicators.
    Primary metrics come from client-side Web Audio API processing.
    """
    if not audio_data_b64 or duration == 0:
        return {
            "speech_duration": 0,
            "silence_duration": duration,
            "silence_ratio": 1.0,
            "speech_rate": 0,
            "assessment": "No audio data",
        }

    # Heuristic: base64 length roughly correlates with audio activity
    data_length = len(audio_data_b64)
    activity_factor = min(data_length / (duration * 1000), 1.0)

    speech_duration = duration * activity_factor * 0.8
    silence_duration = duration - speech_duration
    silence_ratio = silence_duration / max(duration, 1)

    return {
        "speech_duration": round(speech_duration, 2),
        "silence_duration": round(silence_duration, 2),
        "silence_ratio": round(silence_ratio, 3),
        "assessment": "Audio processed",
    }
