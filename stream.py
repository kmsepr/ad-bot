import requests
import subprocess
from flask import Flask, Response

app = Flask(__name__)

# Example: Streaming from a given radio URL
RADIO_URL = "http://your-radio-stream-url"

@app.route('/stream')
def stream():
    def generate():
        process = subprocess.Popen(
            ['ffmpeg', '-i', RADIO_URL, '-f', 'mp3', '-'],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        while True:
            chunk = process.stdout.read(1024)
            if not chunk:
                break
            yield chunk

    return Response(generate(), mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)