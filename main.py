from flask import Flask, request, jsonify
import speech_recognition as sr


app = Flask(__name__)

def recognize_speech(audio_file):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio, language="fa-IR")
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio"
    except sr.RequestError:
        return "API unavailable"

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    audio_file = request.files['file']
    
    try:
        text = recognize_speech(audio_file)
        print(text)
        return jsonify({"text": text}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    
    
    # vosk-model-small-fa-0.5.zip
