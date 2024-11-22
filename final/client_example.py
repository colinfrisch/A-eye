import requests, time
from PIL import Image


# Client makes a POST request with an image and a folder
url = 'http://127.0.0.1:5000/process'
image_path = 'media/test.jpg'
sound_path = 'media/Enregistrement.wav'
mode = 'instruct'


data = {
    'image_path': image_path,
    'sound_folder': sound_path,
    'mode': mode,
}

start = time.time()
response = requests.post(url, data)



print(time.time()-start,response.json()['text'])  # This will print the result from the server
