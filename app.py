import os
import re
import tempfile
from flask import Flask, render_template, request, jsonify, send_file
from yt_dlp import YoutubeDL

app = Flask(__name__)

# Opciones para búsqueda
SEARCH_OPTS = {
    'quiet': True,
    'skip_download': True,
    'format': 'bestaudio',
    'noplaylist': True,
    'extract_flat': False,
    'nocheckcertificate': True,  # 👈 Ignorar verificación SSL esto estaba causando error de certificado ssl al tratar de conectar con la API ademas se comezó a usar un falso user agents
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/115.0.0.0 Safari/537.36'
}

# Opciones para descarga FLAC
YDL_OPTS_DOWNLOAD = {
    'format': 'bestaudio/best',
    'nocheckcertificate': True,  # 👈 Ignorar verificación SSL
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'flac',
        'preferredquality': '0',
    }]
}

# Opciones para descarga MP3
YDL_OPTS_DOWNLOAD_MP3 = {
    'format': 'bestaudio/best',
    'nocheckcertificate': True,  # 👈 Ignorar verificación SSL
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

def extract_video_id(query):
    patterns = [
        r'(?:youtube\.com/watch\?v=)([\w-]{11})',
        r'(?:youtu\.be/)([\w-]{11})',
        r'(?:youtube\.com/shorts/)([\w-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return match.group(1)
    return None

# Ruta para búsqueda
@app.route('/api/search')
def api_search():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({"error": "No query provided"}), 400

    results = []
    
    video_id = extract_video_id(query)
    if video_id:
        try:
            with YoutubeDL(SEARCH_OPTS) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                if info:
                    results.append({
                        'id': info.get('id'),
                        'title': info.get('title'),
                        'duration': info.get('duration'),
                        'thumbnail': info.get('thumbnail'),
                        'audio_url': info.get('url')
                    })
        except Exception as ex:
            return jsonify({"error": str(ex)}), 500
    else:
        try:
            with YoutubeDL(SEARCH_OPTS) as ydl:
                info = ydl.extract_info(f"ytsearch4:{query}", download=False)
                entries = info.get('entries', []) if info else []

                for e in entries:
                    results.append({
                        'id': e.get('id'),
                        'title': e.get('title'),
                        'duration': e.get('duration'),
                        'thumbnail': e.get('thumbnail'),
                        'audio_url': e.get('url')
                    })
        except Exception as ex:
            return jsonify({"error": str(ex)}), 500

    return jsonify(results)

def is_valid_video_id(video_id):
    return re.match(r'^[\w-]{11}$', video_id) is not None

# Descargar FLAC
@app.route('/download/<video_id>')
def download(video_id):
    if not is_valid_video_id(video_id):
        return "Invalid video ID", 400

    url = f"https://www.youtube.com/watch?v={video_id}"
    tmpdir = tempfile.mkdtemp()
    try:
        opts = YDL_OPTS_DOWNLOAD.copy()
        opts['outtmpl'] = os.path.join(tmpdir, '%(title)s.%(ext)s')
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.flac'
        return send_file(filename, as_attachment=True, download_name=f"{info.get('title', 'audio')}.flac")
    except Exception as e:
        print(f"Error: {e}")
        return "Error downloading file", 500
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)

# Descargar MP3
@app.route('/download-mp3/<video_id>')
def download_mp3(video_id):
    if not is_valid_video_id(video_id):
        return "Invalid video ID", 400

    url = f"https://www.youtube.com/watch?v={video_id}"
    tmpdir = tempfile.mkdtemp()
    try:
        opts = YDL_OPTS_DOWNLOAD_MP3.copy()
        opts['outtmpl'] = os.path.join(tmpdir, '%(title)s.%(ext)s')
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
        return send_file(filename, as_attachment=True, download_name=f"{info.get('title', 'audio')}.mp3")
    except Exception as e:
        print(f"Error: {e}")
        return "Error downloading file", 500
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == '__main__':
    app.run(debug=False)
