import re

FILLER_WORDS = [
    "um", "uh", "like", "you know", "basically", "literally", "actually",
    "so", "right", "okay", "well", "kind of", "sort of", "i mean",
    "hmm", "er", "ah", "just", "really", "very"
]

STRONG_WORDS = [
    "implemented", "developed", "designed", "achieved", "improved",
    "optimized", "led", "managed", "created", "built", "solved",
    "analyzed", "delivered", "increased", "reduced", "collaborated",
    "architected", "deployed", "automated", "integrated"
]

TECHNICAL_INDICATORS = [
    "algorithm", "database", "api", "framework", "architecture",
    "optimization", "scalability", "performance", "security", "testing",
    "deployment", "ci/cd", "microservices", "docker", "kubernetes",
    "machine learning", "data", "model", "analysis", "pipeline"
]


def analyze_speech(text: str, filler_count: int = None, word_count: int = None) -> dict:
    if not text or text.strip() == "":
        return {
            "word_count": 0,
            "filler_count": 0,
            "filler_ratio": 0,
            "unique_words": 0,
            "vocabulary_richness": 0,
            "strong_action_words": 0,
            "technical_terms": 0,
            "sentence_count": 0,
            "avg_sentence_length": 0,
            "clarity_score": 0,
            "content_score": 0,
            "assessment": "No answer provided",
            "fillers_found": [],
            "strong_words_found": [],
        }

    text_lower = text.lower().strip()
    words = re.findall(r"\b\w+\b", text_lower)
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # Word metrics
    actual_word_count = word_count if word_count else len(words)
    unique_words = len(set(words))
    vocab_richness = round(unique_words / max(actual_word_count, 1) * 10, 1)

    # Filler analysis
    fillers_found = []
    if filler_count is not None:
        actual_filler_count = filler_count
    else:
        actual_filler_count = 0
        for filler in FILLER_WORDS:
            pattern = r"\b" + re.escape(filler) + r"\b"
            matches = re.findall(pattern, text_lower)
            if matches:
                actual_filler_count += len(matches)
                fillers_found.append(filler)

    filler_ratio = round(actual_filler_count / max(actual_word_count, 1), 3)

    # Strong action words
    strong_found = []
    for word in STRONG_WORDS:
        if re.search(r"\b" + word + r"\b", text_lower):
            strong_found.append(word)

    # Technical terms
    tech_count = 0
    for term in TECHNICAL_INDICATORS:
        if term in text_lower:
            tech_count += 1

    # Sentence metrics
    sentence_count = len(sentences)
    avg_sentence_length = round(actual_word_count / max(sentence_count, 1), 1)

    # Clarity score (0-10)
    clarity = 10.0
    if filler_ratio > 0.15:
        clarity -= 3
    elif filler_ratio > 0.08:
        clarity -= 1.5
    if avg_sentence_length > 30:
        clarity -= 1.5
    elif avg_sentence_length < 5 and sentence_count > 2:
        clarity -= 1
    clarity = max(0, min(10, clarity))

    # Content score (0-10)
    content = 5.0
    if actual_word_count >= 100:
        content += 2
    elif actual_word_count >= 50:
        content += 1
    content += min(len(strong_found) * 0.5, 2)
    content += min(tech_count * 0.3, 1.5)
    content += min(vocab_richness * 0.1, 1)
    content = max(0, min(10, round(content, 1)))

    # Assessment
    if actual_word_count < 20:
        assessment = "Very short response — try to elaborate more on your answers."
    elif actual_word_count < 50:
        assessment = "Brief response — consider adding examples and details."
    elif filler_ratio > 0.15:
        assessment = "Good content length but excessive filler words detected — practice speaking more cleanly."
    elif clarity >= 8 and content >= 7:
        assessment = "Excellent response — clear, structured, and detailed."
    elif content >= 7:
        assessment = "Good content — work on clarity and reducing filler words."
    else:
        assessment = "Decent response — add more technical depth and concrete examples."

    return {
        "word_count": actual_word_count,
        "filler_count": actual_filler_count,
        "filler_ratio": filler_ratio,
        "unique_words": unique_words,
        "vocabulary_richness": round(vocab_richness, 1),
        "strong_action_words": len(strong_found),
        "technical_terms": tech_count,
        "sentence_count": sentence_count,
        "avg_sentence_length": avg_sentence_length,
        "clarity_score": round(clarity, 1),
        "content_score": content,
        "assessment": assessment,
        "fillers_found": fillers_found[:5],
        "strong_words_found": strong_found[:5],
    }
