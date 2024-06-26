import cld3
from flask import Flask, request, send_file, jsonify
import torch
from transformers import pipeline
import os
import json
import base64
app = Flask(__name__)

def remember_language(lang: str):
    with open('last-language', 'w') as f:
        f.writelines([lang])

def last_language() -> str | None:
    if not os.path.exists('last-language'):
        return None

    with open('last-language', 'r') as f:
        return f.readline()

device = "cuda:0" if torch.cuda.is_available() else "cpu"

PIPE = pipeline(
  "automatic-speech-recognition",
  model="openai/whisper-medium",
  chunk_length_s=30,
  device=device,
)

@app.route('/v1/images/generations', methods=['POST'])
def image():
    data = request.get_json()  # Get the JSON input from the POST request
    prompt = data['prompt']  # Extract the 'input' field
        
    os.system(f"./gen_image.sh \"{prompt}\"")
    
    file_text = open('image.png', 'rb')
    file_read = file_text.read()
    b64img = base64.encodebytes(file_read).decode('utf-8')
    o = {"data": [{'b64_json': b64img}]}
    return jsonify(o)

@app.route('/v1/audio/speech', methods=['POST'])
def speech():
    data = request.get_json()  # Get the JSON input from the POST request
    text = data['input']  # Extract the 'input' field
    prediction = cld3.get_language(text)
    lang = prediction.language

    if (prediction.is_reliable):
        remember_language(lang)
    else:
        last_lang = last_language()
        if not last_language == None:
            lang = last_lang

    
    with open('textfile.txt', 'w') as f:  # Write the extracted text to a file
        f.write(text)
        
    os.system(f"./tts.sh {lang}")
    
    return send_file('output.wav', mimetype='audio/x-wav')  # Return the audio file in the HTTP response


@app.route('/v1/audio/transcriptions', methods=['POST'])
def transcribe():
    file = request.files['file']
    file.save('upload.wav')
    transcription = PIPE('upload.wav')

    return json.dumps(transcription), 200


if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")
    app.config['UPLOAD_FOLDER'] = '.'
