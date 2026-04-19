import tempfile
import os

try:
    import yt_dlp
except ImportError:
    yt_dlp = None


def download_youtube_audio(url):
    url = (url or "").strip()
    if not url:
        return None
    if yt_dlp is None:
        print("yt-dlp not installed.")
        return None
    out_dir = tempfile.mkdtemp()
    out_tmpl = os.path.join(out_dir, "audio.%(ext)s")
    opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": out_tmpl,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        for name in os.listdir(out_dir):
            path = os.path.join(out_dir, name)
            if os.path.isfile(path):
                return path
        return None
    except Exception as e:
        print("YouTube download error:", e)
        try:
            for name in os.listdir(out_dir):
                os.remove(os.path.join(out_dir, name))
            os.rmdir(out_dir)
        except Exception:
            pass
        return None
