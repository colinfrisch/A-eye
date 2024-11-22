from PIL import Image
from openai import OpenAI
import base64
from io import BytesIO
from API_setup import *


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


def encode_image(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string


def messages(base64_img):

    return [
        {
            "role": "system",
            "content": """You are a helpful assistant expert in helping blind people in their day-to-day life.
            You are his eyes so everything you see is from his point of view.""",
            },
            
        {"role": "user",
         "content": [{"type": "text", "text": "What should i know about what is in front of me ? Be very concise (20 words max)"},{"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},},],},
            ]




def process_image(image_path):
    result=[]

    img = Image.open(image_path)
    img_resized = resize_image(img, width=600)
    base64_img = encode_image(img_resized)

    response = client.chat.completions.create(
    messages=messages(base64_img),
    model=MODEL,
    stream = False
    )

    
    
    return response.choices[0].message.content
