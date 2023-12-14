# oai_client_async.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()


def get_openai_client():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key is not set. Please set it in the environment.")
    return openai.AsyncOpenAI(api_key=openai_api_key)


# import openai
# import threading
# import os
# import instructor
# import functools

# from dotenv import load_dotenv

# load_dotenv()

# client_lock = threading.Lock()
# client = None


# @functools.lru_cache
# def get_openai_client():
#     # Check if the API key is set
#     api_key = openai.api_key or os.getenv('OPENAI_API_KEY')
#     if api_key is None:
#         raise ValueError("OpenAI API key is not set. Please set it using set_openai_key.")
#     return instructor.apatch(openai.AsyncOpenAI(api_key=api_key))


# def set_openai_key(key):
#     if not key:
#         raise ValueError("Invalid API key. The API key cannot be empty.")
#     openai.api_key = key
