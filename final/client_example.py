import requests, time, base64
from PIL import Image
from io import BytesIO

def encode_image(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string

# Client makes a POST request with an image and a folder
url = 'http://127.0.0.1:5000/instruct'
image_path = 'media/test.jpg'
sound_path = 'media/Enregistrement.wav'
mode = 'instruct'

base64_imgs = [
    encode_image(Image.open(f'media/{i}-min.jpg')) for i in range(1, 7)
]

with open(sound_path, "rb") as file:
    wav_data = file.read()
    sound_b64 = base64.b64encode(wav_data).decode('utf-8')  # Correct encoding to string

data = {    
    'image': base64_imgs,
    'sound': sound_b64,
    'mode': mode,
}

headers = {'Content-Type': 'application/json'}  # Specify JSON content type

start = time.time()
response = requests.post(url, json=data, headers=headers)  # Use `json` argument

print(time.time() - start, response.json()["text"])  # This will print the result from the server

sound_data = base64.b64decode(response.json()['audio_b64'])
with open("final_sound.wav", "wb") as sound_file:
    sound_file.write(sound_data)
