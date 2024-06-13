import cld3
from flask import Flask, request, send_file
import os
app = Flask(__name__)

@app.route('/v1/audio/speech', methods=['POST'])
def speech():
    data = request.get_json()  # Get the JSON input from the POST request
    text = data['input']  # Extract the 'input' field
    prediction = cld3.get_language(text)
    lang = prediction.language

    
    with open('textfile.txt', 'w') as f:  # Write the extracted text to a file
        f.write(text)
        
    os.system(f"./tts.sh {lang}")
    
    return send_file('output.wav', mimetype='audio/x-wav')  # Return the audio file in the HTTP response

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")
