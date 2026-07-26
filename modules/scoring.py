def calculate_scores(video_metrics: dict, audio_metrics: dict, speech_metrics: dict) -> dict:
    """Calculate multi-dimensional scores from all analysis modules."""

    # --- Confidence Score (0-10) ---
    face_ratio = video_metrics.get("face_detected_ratio", 0.7)
    silence_ratio = audio_metrics.get("silence_ratio", 0.3)
    filler_ratio = speech_metrics.get("filler_ratio", 0.05)

    confidence = 5.0
    confidence += face_ratio * 3          # camera presence
    confidence -= silence_ratio * 3       # pauses hurt confidence
    confidence -= filler_ratio * 10       # fillers hurt confidence
    confidence += min(speech_metrics.get("strong_action_words", 0) * 0.3, 1.5)
    confidence = max(0, min(10, round(confidence, 1)))

    # --- Communication Score (0-10) ---
    word_count = speech_metrics.get("word_count", 0)
    clarity = speech_metrics.get("clarity_score", 5)
    vocab = speech_metrics.get("vocabulary_richness", 5)

    communication = clarity * 0.5
    communication += vocab * 0.3
    if word_count >= 80:
        communication += 2
    elif word_count >= 40:
        communication += 1
    communication += min(speech_metrics.get("sentence_count", 0) * 0.1, 1)
    communication = max(0, min(10, round(communication, 1)))

    # --- Engagement Score (0-10) ---
    eye_contact = video_metrics.get("eye_contact_score", 5)
    posture = video_metrics.get("posture_score", 5)

    engagement = eye_contact * 0.5 + posture * 0.3
    speech_duration = audio_metrics.get("speech_duration", 0)
    total = speech_duration + audio_metrics.get("silence_duration", 0)
    if total > 0:
        speech_ratio = speech_duration / total
        engagement += speech_ratio * 2
    engagement = max(0, min(10, round(engagement, 1)))

    # --- Fluency Score (0-10) ---
    speech_rate = audio_metrics.get("speech_rate", 120)
    avg_sentence = speech_metrics.get("avg_sentence_length", 10)

    fluency = 7.0
    # ideal speech rate ~120-160 wpm
    if 100 <= speech_rate <= 160:
        fluency += 1.5
    elif speech_rate < 80 or speech_rate > 200:
        fluency -= 2
    fluency -= filler_ratio * 8
    if silence_ratio < 0.2:
        fluency += 1
    elif silence_ratio > 0.5:
        fluency -= 2
    fluency = max(0, min(10, round(fluency, 1)))

    # --- Content Score (0-10) ---
    content = speech_metrics.get("content_score", 5)

    return {
        "confidence": confidence,
        "communication": communication,
        "engagement": engagement,
        "fluency": fluency,
        "content": content,
    }


def get_grade(score: float) -> str:
    if score >= 9:
        return "A+"
    elif score >= 8:
        return "A"
    elif score >= 7:
        return "B+"
    elif score >= 6:
        return "B"
    elif score >= 5:
        return "C"
    elif score >= 4:
        return "D"
    else:
        return "F"


def get_performance_level(score: float) -> str:
    if score >= 8.5:
        return "Excellent"
    elif score >= 7:
        return "Good"
    elif score >= 5.5:
        return "Average"
    elif score >= 4:
        return "Below Average"
    else:
        return "Needs Improvement"
