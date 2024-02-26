from openai import OpenAI
from keys import api_key
import openai

client = OpenAI(api_key=api_key)

def generateImage(prompt):

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        return(response.data[0].url)

    except openai.BadRequestError:
        return("Your request was rejected as a result of our safety system. Your prompt may contain text that is not allowed by our safety system.")

    except Exception:
        return("An unexpected error occurred!")
    