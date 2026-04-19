================================================================================
  AI LECTURE CONTENT GENERATOR (English Only)
================================================================================

A Flask web app that extracts speech from MP4 videos or YouTube links,
transcribes it, and lets you view or download the content as PDF.
Optional: simplify transcript as bullet points.

--------------------------------------------------------------------------------
HOW TO INSTALL
--------------------------------------------------------------------------------

1. Open Command Prompt (cmd) or PowerShell.

2. Go to the project folder:
   cd path\to\vino
   Example:  cd E:\DK\vino

3. Install dependencies from requirements.txt:
   pip install -r requirements.txt

   Or install one by one:
   pip install flask
   pip install reportlab
   pip install moviepy
   pip install imageio-ffmpeg
   pip install faster-whisper
   pip install yt-dlp

4. (Optional) FFmpeg is recommended for moviepy and yt-dlp.
   If not installed, get it from https://ffmpeg.org/ and add to PATH.

--------------------------------------------------------------------------------
HOW TO RUN
--------------------------------------------------------------------------------

1. In the same folder (e.g. E:\DK\vino), run:
   python app.py

2. Open a browser and go to:
   http://127.0.0.1:5000

3. To stop the server, press Ctrl+C in the terminal.

--------------------------------------------------------------------------------
HOW TO USE
--------------------------------------------------------------------------------

- YouTube link: Paste a YouTube URL in the text box and click
  "Extract and Transcribe". The app will download the audio, transcribe it,
  and show the transcript.

- MP4 upload: Click "Select MP4 file", choose a video, then click
  "Extract and Transcribe". The app will extract audio, transcribe it,
  and show the transcript.

- Simplify as bullet points: Check "Simplify as bullet points" before
  submitting to convert the transcript into short bullet points for
  easier reading. The same content is shown on the page and in the PDF.

- Download PDF: After content is generated, click "Download PDF" to get
  the same text as a PDF file.

- Generation time is shown (e.g. "Generated in 12.3 seconds").
  A loading spinner appears while the server is processing.

--------------------------------------------------------------------------------
REQUIREMENTS
--------------------------------------------------------------------------------

- Python 3.8 or higher
- Internet connection only for YouTube links (transcription runs locally)
- For best results: FFmpeg installed and on system PATH

--------------------------------------------------------------------------------
PROJECT STRUCTURE
--------------------------------------------------------------------------------

app.py                 Main Flask application
templates/
  index.html            Web interface
modules/
  video_to_audio.py     Extract audio from MP4 (moviepy)
  speech_to_text.py     Transcribe audio (faster-whisper)
  pdf_generator.py      Generate PDF (reportlab)
  youtube_download.py   Download audio from YouTube (yt-dlp)
  simplify_content.py   Convert transcript to bullet points
requirements.txt        Pip dependencies

================================================================================
