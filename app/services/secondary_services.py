# app/services/secondary_services.py
import os
import asyncio

from app.threads.async_thread import AsyncThread
from app.utils.assistants import get_assistant


async def process_with_psychologist(suggestion):
    psychologist_id = os.getenv("PSYCHOLOGIST_ID")
    psychologist_thread = AsyncThread(psychologist_id)

    await psychologist_thread.create_thread()
    await psychologist_thread.send_message(suggestion)
    psychology_result = await psychologist_thread.await_response()
    return psychology_result


async def process_with_wardrobe(suggestion, user_input):
    wardrobe_id = os.getenv("WARDROBE_ID")
    wardrobe_thread = AsyncThread(wardrobe_id)

    await wardrobe_thread.create_thread()
    await wardrobe_thread.send_message(f"{suggestion}\n{user_input}")
    product_info = await wardrobe_thread.await_response()
    return product_info
