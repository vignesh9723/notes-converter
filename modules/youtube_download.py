import tempfile
import os
import yt_dlp

def download_youtube_audio(url):
    url = (url or "").strip()
    if not url:
        return None

    # Cookies file path (Main folder-il ulla file-ai edukkum)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    COOKIE_PATH = os.path.join(BASE_DIR, 'youtube_cookies.txt')

    out_dir = tempfile.mkdtemp()
    out_tmpl = os.path.join(out_dir, "audio.%(ext)s")

    opts = {
    # Specific format-ai thavirtthu best audio-vai edukkavum
        "format": "bestaudio/best", 
        "outtmpl": out_tmpl,
        "quiet": True,
        "no_warnings": True,
        "cookiefile": COOKIE_PATH,
        # Audio-vai MP3-aaga maatra indha section miguvum mukkiyam
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        
        # Download aanavudan file-ai kandupidippom
        for name in os.listdir(out_dir):
            path = os.path.join(out_dir, name)
            if os.path.isfile(path):
                return path
        return None

    except Exception as e:
        print(f"YouTube download error: {e}")
        # Error vandhaal andha folder-ai clean seiyalaam
        try:
            for name in os.listdir(out_dir):
                os.remove(os.path.join(out_dir, name))
            os.rmdir(out_dir)
        except:
            pass
        return None
