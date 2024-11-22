import requests
from PIL import Image


# Client makes a POST request with an image and a folder
url = 'http://127.0.0.1:5000/process'
image_path = 'media/test.jpg'
sound_path = None
mode = 'allaround'

data = {
    'image_path': image_path,
    'sound_folder': sound_path,
    'mode': mode,
}

response = requests.post(url, image, sound, mode)
print(response.json())  # This will print the result from the server
