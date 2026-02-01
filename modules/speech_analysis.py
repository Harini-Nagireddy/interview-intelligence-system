import json
import wave
from vosk import Model, KaldiRecognizer

FILLER_WORDS = ["uh", "um", "like", "you know", "ah", "er"]

def analyze_speech(audio_path, model_path="assets/vosk-model-small-en-us-0.15"):
    wf = wave.open(audio_path, "rb")
    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    transcript = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            transcript += " " + result.get("text", "")

    final_result = json.loads(rec.FinalResult())
    transcript += " " + final_result.get("text", "")
    transcript = transcript.strip()

    words = transcript.split()
    word_count = len(words)

    filler_count = sum(transcript.count(f) for f in FILLER_WORDS)

    # Simple structure heuristic
    if word_count > 120:
        structure = "Well Structured"
    elif word_count > 50:
        structure = "Moderately Structured"
    else:
        structure = "Poorly Structured"

    return {
        "transcript": transcript,
        "word_count": word_count,
        "filler_words_count": filler_count,
        "speech_structure": structure
    }
