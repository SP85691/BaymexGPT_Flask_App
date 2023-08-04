import openai
import os
import numpy as np
import base64
import cv2
import dotenv

dotenv.load_dotenv()

# Import data from .env file using os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def openai_prompt(question):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": str(question)
            },
        ],
        temperature=1,
        max_tokens=700,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
     # Access the 'choices' field from the response
    choices = response['choices']

    # Get the 'message' field from the first item in 'choices'
    if choices and 'message' in choices[0]:
        message = choices[0]['message']

        # Extract the content (response) from the 'message'
        if 'content' in message:
            content = message['content']
            return content

    # Return None if content not found
    return None

def text_to_image_converter(text):
        print(OPENAI_API_KEY)
        openai.api_key = OPENAI_API_KEY
        response = openai.Image.create(
                prompt = text,
                n = 1,
                size = "1024x1024",
                response_format = "b64_json"
        )
        im_bytes = base64.b64decode(response['data'][0]['b64_json'])
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        img = cv2.imdecode(im_arr, cv2.IMREAD_COLOR)
        cv2.imwrite(os.path.join("app/static/", "img.png"), img)
        