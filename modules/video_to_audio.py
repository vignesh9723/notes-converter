from moviepy import VideoFileClip
import tempfile
import os


def extract_audio(video_path):
    audio_path = None
    try:
        wav_fd, audio_path = tempfile.mkstemp(suffix=".wav")
        os.close(wav_fd)
        with VideoFileClip(video_path) as clip:
            if clip.audio is None:
                os.remove(audio_path)
                return None
            clip.audio.write_audiofile(audio_path)
        return audio_path
    except Exception as e:
        print("Audio extraction error:", e)
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except Exception:
                pass
        return None
