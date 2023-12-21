# oai_client_async.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()


def get_openai_async_client():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key is not set. Please set it in the environment.")
    return openai.AsyncOpenAI(api_key=openai_api_key)


def get_openai_client():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key is not set. Please set it in the environment.")
    return openai.OpenAI(api_key=openai_api_key)


client_async = get_openai_async_client()
client = get_openai_client()
