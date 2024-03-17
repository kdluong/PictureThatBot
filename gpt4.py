from openai import OpenAI
import requests
import io
import os

api_key = os.environ["api_key"]

# Generate Image using Tweet as Prompt


def generate_image(api, prompt):

    try:

        # Attempt to authenticate user

        client = OpenAI(api_key=api_key)

        # Generate Image

        response = client.images.generate(
            model="dall-e-3", prompt=prompt, size="1024x1024", quality="standard", n=1
        )

        # Convert URL to Bytes inorder to tweet

        img_data = requests.get(response.data[0].url).content
        img_data_file_like = io.BufferedReader(io.BytesIO(img_data))

        return api.media_upload(filename="temp.jpg", file=img_data_file_like)

    except Exception as e:
        return "failed"
