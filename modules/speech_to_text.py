_model = None


def transcribe_audio(audio_path):
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, info = _model.transcribe(audio_path, beam_size=1)
    full_text = ""
    for segment in segments:
        full_text += segment.text + " "
    return full_text.strip()
