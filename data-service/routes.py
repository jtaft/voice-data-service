from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import os
import random
from json.decoder import JSONDecodeError

AUDIO_DATA_FILE = '/home/jay/karas/voice-data-service/audio-data.json'
AUDIO_FOLDER = '/home/jay/karas/voice-data-service/audio/'

app = Flask(__name__)

@app.route('/audio', methods=['GET', 'POST'])
def save_audio():
    print(request.headers)
    if request.method == 'GET':
        return 'Post some data!'
    elif request.method == 'POST':
        if 'file' in request.files and 'audio-txt' in request.form:
            audio_txt = request.form['audio-txt']
            file = request.files['file']
            if file and audio_txt:
                filename = secure_filename(file.filename)
                print(filename)
                print(audio_txt)
                with open(AUDIO_DATA_FILE, 'r+') as audio_data_file:
                    try:
                        jf = json.load(audio_data_file)
                    except JSONDecodeError:
                        print('decode error')
                        jf = {}
                    print(json.dumps(jf))
                    audio_data_file.seek(0)
                    audio_data_file.truncate()
                    jf[str(len(jf))] = audio_txt
                    json.dump(jf,audio_data_file)
                    file.save(os.path.join(AUDIO_FOLDER, (str(len(jf) - 1) + '.wav')))
                return 'Success'

@app.route('/trainingtext', methods=['GET'])
def get_training_text():
    print(request.headers)
    if request.method == 'GET':
        with open(AUDIO_DATA_FILE, 'r') as audio_data_file:
            try:
                jf = json.load(audio_data_file)
            except JSONDecodeError:
                return 'Yes'
            return random.choice(['Yes','No'])
            #yes = 0
            #no = 0
            #for key, value in jf.items():
            #    if value.lower() == 'yes':
            #        yes += 1
            #    if value.lower() == 'no':
            #        no +=1
            #if no < yes:
            #    return 'No'
            #return 'Yes'
            print(json.dumps(jf))
