import base64, os, time, whisper, pyttsx3
from PIL import Image
from openai import OpenAI
from io import BytesIO
from API_setup import *
from flask import Flask, request, jsonify

app = Flask(__name__)

#whisper init
whisper_model = whisper.load_model('tiny')


# Initialize the pyttsx3 engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def resize_image(image, width=None, height=None, keep_ratio=True):

    # Open the image if a path is provided
    if isinstance(image, str):
        with Image.open(image) as img:
            img = img.copy()  # Avoids issues with closed files
    elif isinstance(image, Image.Image):
        img = image
    else:
        raise ValueError("Invalid input: 'image' must be a file path or PIL.Image.Image object.")

    # Ensure at least one of width or height is specified
    if not width and not height:
        raise ValueError("At least one of 'width' or 'height' must be specified.")

    # Maintain aspect ratio if required
    if keep_ratio:
        original_width, original_height = img.size
        if width and not height:  # Calculate height preserving ratio
            height = int((width / original_width) * original_height)
        elif height and not width:  # Calculate width preserving ratio
            width = int((height / original_height) * original_width)
        img.thumbnail((width, height), Image.LANCZOS)
    else:
        # Resize without preserving aspect ratio
        if not width or not height:
            raise ValueError("Both 'width' and 'height' must be specified when keep_ratio=False.")
        img = img.resize((width, height), Image.LANCZOS)

    return img


def encode_image(image_path):
    img = Image.open(image_path)
    img_resized = resize_image(img, width=600)
    buffered = BytesIO()
    img_resized.save(buffered, format="JPEG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string


def messages(base64_img,type='allaround',prompt="What should i know about what is in front of me ? Be very concise (20 words max)."):

    if type == 'allaround' or type == 'instruct':
        return [
            {
                "role": "system",
                "content": """You are a helpful assistant expert in helping blind people in their day-to-day life.
                You are his eyes so everything you see is from his point of view.""",
                },
                
            {"role": "user",
            "content": [{"type": "text", "text": prompt + "Be very concise"},{"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},},],},
                ]
    
    if type == 'ocr':
        return [
            {
                "role": "system",
                "content": """You are an OCR transcribing machine""",
                },
                
            {"role": "user",
            "content": [{"type": "text", "text": """Act as an OCR assistant. Analyze the provided image and:
                        1. Recognize all visible text in the image as accurately as possible.
                        2. Maintain the original structure and formatting of the text.
                        3. If any words or phrases are unclear, indicate this with [unclear] in your transcription.
                        Provide only the transcription without any additional comments. Don't transcribe anything that is not the text you see. Your answer should be in markdown format"""},{"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},},],},
                ]


def text_to_speech(text,output_path):
    engine.setProperty('rate', 150)
    engine.save_to_file(text, output_path)
    engine.runAndWait()


def speech_to_text_whisper(audio_file):    
    start=time.time()
    result = whisper_model.transcribe(audio_file)
    #print(time.time()-start, result["text"])
    return result["text"]

#Utilisation
def process_input(image_path,audio_file=None):

    base64_img = encode_image(image_path) #resizes and base64-encodes the image

    if audio_file==None :
        response = client.chat.completions.create(messages=messages(base64_img,'allaround'),model=MODEL,stream = False)
    
    else :
        prompt = speech_to_text_whisper(audio_file)
        response = client.chat.completions.create(messages=messages(base64_img,'instruct',prompt),model=MODEL,stream = False)


    audio_path ='output.wav'
    text_to_speech(engine,response,audio_path)
  
    return {"text": response.choices[0].message.content, "audio_url": audio_path} 





@app.route('/process', methods=['POST'])
def process_data():

    image_path = request.image_path
    sound_path = request.sound_path
    mode = request.mode
    
    if mode == 'allaround':
        result = process_input(image_path)
    elif mode == 'instruct':
        result = process_input(image_path,sound_path)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)