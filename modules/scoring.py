def label(score):
    if score >= 80:
        return "Strong"
    elif score >= 50:
        return "Moderate"
    else:
        return "Weak"


def score_camera_presence(camera_presence):
    # camera_presence is %
    score = min(100, max(0, camera_presence))
    return score, label(score)


def score_voice(speech_ratio, speech_pace):
    # speech_ratio = speech_duration / total_audio_duration
    score = int(speech_ratio * 100)

    if speech_pace == "Fast":
        score -= 10
    elif speech_pace == "Slow":
        score -= 15

    score = max(0, min(100, score))
    return score, label(score)


def score_communication(word_count, filler_count, structure):
    score = 0

    # Word count contribution
    if word_count >= 120:
        score += 40
    elif word_count >= 60:
        score += 30
    else:
        score += 15

    # Filler words penalty
    if filler_count <= 3:
        score += 30
    elif filler_count <= 7:
        score += 20
    else:
        score += 10

    # Structure score
    if structure == "Well Structured":
        score += 30
    elif structure == "Moderately Structured":
        score += 20
    else:
        score += 10

    score = min(100, score)
    return score, label(score)


def final_interview_score(camera_score, voice_score, communication_score):
    final = int(
        0.35 * camera_score +
        0.30 * voice_score +
        0.35 * communication_score
    )
    return final, label(final)
