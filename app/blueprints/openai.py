import openai
import os
import numpy as np
import base64
import cv2

OPENAI_API_KEY = "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"

def openai_prompt(question):
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=1,
            max_tokens=1080,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,       
            stop=[" Human:", " AI:"]
            )
    return response["choices"][0]["text"]

def text_to_image_converter(text):
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