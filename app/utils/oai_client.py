# app/utils/openai_client.py
from openai import OpenAI
from dotenv import load_dotenv
import os


def get_openai_client():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=openai_api_key)


# from dotenv import load_dotenv
# import os
# import openai

# def get_openai_client():
#     load_dotenv()
#     api_key = os.getenv("OPENAI_API_KEY")
#     if api_key is None:
#         raise ValueError("OpenAI API key is not set. Please set it using set_openai_key.")
#     openai.api_key = api_key
#     return openai
