import requests, time, base64
from PIL import Image


# Client makes a POST request with an image and a folder
url = 'http://127.0.0.1:5000/process'
image_path = 'media/test.jpg'
sound_path = 'media/Enregistrement.wav'
mode = 'instruct'

with open(sound_path, "rb") as file:
    wav_data = file.read()
    sound_b64 = base64.b64encode(wav_data)

with open(image_path, "rb") as file:
    img_data = file.read()
    image_b64 = base64.b64encode(img_data)




data = {    
    'image': image_b64,
    'sound': sound_b64,
    'mode': mode,
}

start = time.time()
response = requests.post(url, data)

print(time.time()-start,response.json().keys())  # This will print the result from the server

sound_data = base64.b64decode(response.json()['audio_b64'])
with open("final_sound.wav", "wb") as sound_file:
        sound_file.write(sound_data)