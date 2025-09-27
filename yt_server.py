from flask import Flask, request, Response
import yt_dlp
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube → MP3 Streamer is running."

@app.route("/stream")
def stream_audio():
    url = request.args.get("url")
    if not url:
        return "No URL provided", 400

    ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']

    ffmpeg = subprocess.Popen([
        'ffmpeg', '-i', audio_url,
        '-f', 'mp3', '-ab', '192k', '-'
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    return Response(ffmpeg.stdout, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
