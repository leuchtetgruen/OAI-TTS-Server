import cld3
from flask import Flask, request, send_file
import os
app = Flask(__name__)

def remember_language(lang: str):
    with open('last-language', 'w') as f:
        f.writelines([lang])

def last_language() -> str | None:
    if not os.path.exists('last-language'):
        return None

    with open('last-language', 'r') as f:
        return f.readline()


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

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")
