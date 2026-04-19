# Required setup:
# python -m pip install flask reportlab moviepy imageio-ffmpeg faster-whisper yt-dlp

from flask import Flask, render_template, request, redirect, url_for, send_file
import tempfile
import os
import time

from modules.video_to_audio import extract_audio
from modules.speech_to_text import transcribe_audio
from modules.pdf_generator import generate_pdf
from modules.youtube_download import download_youtube_audio
from modules.simplify_content import simplify_content

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

stored_content = ""
stored_content_as_bullets = False


@app.route("/", methods=["GET", "POST"])
def index():
    global stored_content, stored_content_as_bullets
    if request.method == "POST":
        youtube_url = (request.form.get("youtube_url") or "").strip()
        file = request.files.get("mp4_file")
        simplify = request.form.get("simplify_content") == "on"
        if youtube_url:
            start_time = time.time()
            audio_path = download_youtube_audio(youtube_url)
            if not audio_path:
                return render_template("index.html", error="YouTube download failed.")
            try:
                transcript = transcribe_audio(audio_path)
                if not transcript or transcript.strip() == "":
                    return render_template("index.html", error="Transcription failed")
                if simplify:
                    transcript = simplify_content(transcript)
                    stored_content_as_bullets = True
                else:
                    stored_content_as_bullets = False
                stored_content = transcript
                elapsed = time.time() - start_time
                return render_template(
                    "index.html",
                    content=transcript,
                    content_as_bullets=simplify,
                    generation_time=round(elapsed, 1),
                )
            finally:
                if audio_path and os.path.exists(audio_path):
                    os.remove(audio_path)
                d = os.path.dirname(audio_path)
                if d and os.path.isdir(d):
                    try:
                        os.rmdir(d)
                    except Exception:
                        pass
        elif file and file.filename and file.filename.lower().endswith(".mp4"):
            start_time = time.time()
            mp4_fd, mp4_path = tempfile.mkstemp(suffix=".mp4")
            try:
                file.save(mp4_path)
                os.close(mp4_fd)
                try:
                    wav_path = extract_audio(mp4_path)
                except Exception:
                    return render_template("index.html", content=None, error="Video processing failed. Ensure moviepy is installed.")
                if not wav_path:
                    return render_template("index.html", error="Audio extraction failed")
                time.sleep(1)
                try:
                    os.remove(mp4_path)
                except Exception as e:
                    print("File deletion error:", e)
                try:
                    transcript = transcribe_audio(wav_path)
                    if not transcript or transcript.strip() == "":
                        return render_template("index.html", error="Transcription failed")
                    if simplify:
                        transcript = simplify_content(transcript)
                        stored_content_as_bullets = True
                    else:
                        stored_content_as_bullets = False
                    stored_content = transcript
                    elapsed = time.time() - start_time
                    return render_template(
                        "index.html",
                        content=transcript,
                        content_as_bullets=simplify,
                        generation_time=round(elapsed, 1),
                    )
                finally:
                    if os.path.exists(wav_path):
                        os.remove(wav_path)
            finally:
                if os.path.exists(mp4_path):
                    try:
                        os.remove(mp4_path)
                    except Exception as e:
                        print("File deletion error:", e)
        else:
            return render_template("index.html", content=None, error="Provide a YouTube link or upload an MP4 file.")
    return render_template("index.html", content=None)


@app.route("/download")
def download():
    global stored_content, stored_content_as_bullets
    if not stored_content:
        return redirect(url_for("index"))
    pdf_path = generate_pdf(stored_content, as_bullets=stored_content_as_bullets)
    return send_file(
        pdf_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="Lecture_Transcript.pdf"
    )


if __name__ == "__main__":
    app.run(debug=False)
