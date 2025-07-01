import tempfile
from flask import Flask, request, send_file, jsonify
from TTS.api import TTS

app = Flask(__name__)

@app.route('/api/tts', methods=['POST'])
def tts_handler():
    data = request.get_json()
    text = data.get('text')
    model_name = data.get('model')

    if not text or not model_name:
        return jsonify({"error": "Missing text or model"}), 400

    try:
        tts = TTS(model_name=model_name, progress_bar=False, gpu=False)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
            tts.tts_to_file(text=text, file_path=fp.name)
            fp.seek(0)
            return send_file(fp.name, mimetype="audio/wav", as_attachment=True, download_name="output.wav")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# For Vercel: expose 'app' as 'handler'
handler = app 