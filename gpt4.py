from openai import OpenAI
from keys import api_key
import requests
import io

client = OpenAI(api_key=api_key)

def generateImage(api, prompt):

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        img_data = requests.get(response.data[0].url).content
        img_data_file_like = io.BufferedReader(io.BytesIO(img_data))

        return api.media_upload(filename="temp.jpg", file=img_data_file_like)

    except Exception as e:
        return 'fail'