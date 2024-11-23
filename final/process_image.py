import base64, os, time, whisper, pyttsx3, json,io
from PIL import Image
from openai import OpenAI
from io import BytesIO
from API_setup import *
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#whisper init
whisper_model = whisper.load_model('tiny')
MODEL = "pixtral-12b-2409"


# Initialize the pyttsx3 engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

json_history_file = 'chat_history.json'
last_interaction_time = None



def messages(base64_imgs,prompt,history,type='instruct'):

    content = [
        {"type": "text", "text": "These images are taken from a video, analyse them as a whole and be very brief in your answer. My prompt is "+prompt}] + [
        {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},
        } for base64_img in base64_imgs
    ]

    if type == 'instruct':
        if history!= [] :
            history = history[-5:]
            return [

                {
                    "role": "system",
                    "content": """  You are a helpful assistant expert in helping blind people in their day-to-day life.
                    You are his eyes so everything you see is from his point of view. Do not forget that the person that you assist does not see anything so don't hesitate to give clear spatial directions respectively to his right and left. Your responses have to be very brief.""",
                    }] +\
                history +\
                [{"role": "user",
                "content": content}]
                    
        else:
            return [

                {
                    "role": "system",
                    "content": """  You are a helpful assistant expert in helping blind people in their day-to-day life.
                    You are his eyes so everything you see is from his point of view. Do not forget that the person that you assist does not see anything so don't hesitate to give clear spatial directions respectively to his right and left. Your responses have to be very concise.""",
                    },
                    
                {"role": "user",
                "content": content},
                    ]
            
def should_reset_history():
    global last_interaction_time
    current_time = time.time()
    if last_interaction_time is None or current_time - last_interaction_time > 100:
        last_interaction_time = current_time  # Met à jour le timestamp
        return True
    last_interaction_time = current_time  # Met à jour le timestamp
    return False

def text_to_speech(text,output_path):
    engine.setProperty('rate', 150)
    engine.save_to_file(text, output_path)
    engine.runAndWait()

    with open(output_path, "rb") as file:
        wav_data = file.read()
    
    return base64.b64encode(wav_data).decode('utf-8')


def speech_to_text_whisper(audio_file):    
    start=time.time()
    result = whisper_model.transcribe(audio_file)
    #print(time.time()-start, result["text"])
    return result["text"]


def process_input(image_b64,audio_file,history=[]):
    global json_history_file

    start = time.time()
    prompt = speech_to_text_whisper(audio_file)
    print(prompt,f'(processing time : {-start + time.time()})')

    print('interracting with model')
    response = client.chat.completions.create(messages=messages(image_b64,prompt,history,'instruct'),model=MODEL,stream = False)

    text_response = response.choices[0].message.content

    history.append({"role": "user",
                "content": prompt})
    
    history.append({"role": "assistant",
                "content": text_response})
    
    with open(json_history_file, "w", encoding="utf-8") as fichier:
        json.dump(history, fichier, indent=4, ensure_ascii=False)

    audio_path ='output.wav'
    sound_b64=text_to_speech(text_response,audio_path)
    print(text_response)

    return {"text": text_response, "audio_b64": sound_b64} 



@app.route('/instruct', methods=['POST'])
def process_data():
    global json_history_file, last_interaction_time

    if should_reset_history():
        history = []
    else:
        if os.path.exists(json_history_file):
            with open(json_history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        else:
            history = []

    data = request.get_json()

    image_b64 = data.get('images')
    sound_b64 = data.get('sound')
    mode = data.get('mode')

    sound_data = base64.b64decode(sound_b64)


    sound_path = "sound.wav"
    with open(sound_path, "wb") as sound_file:
        sound_file.write(sound_data)  # Write the decoded sound data to a file


    result = process_input(image_b64, sound_path, history)
    play_audio_from_base64(result["audio_b64"])

    return jsonify(result)

def play_audio_from_base64(base64_audio):
    # Decode the base64 string to binary data
    audio_data = base64.b64decode(base64_audio)

    # Save the binary data to a temporary file (WAV format for this example)
    os.remove("temp_audio.wav")
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_data)

if __name__ == '__main__':
    app.run(debug=True)