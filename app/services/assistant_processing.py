# orchestrator_service.py
import os
import asyncio
from dotenv import load_dotenv

from app.threads.async_thread import AsyncThread

# from app.utils.assistants import get_assistant

load_dotenv()


async def process_with_orchestrator(user_input):
    orchestrator_id = os.getenv("ORCHESTRATOR_ASSISTANT_ID")
    orchestrator_thread = AsyncThread(orchestrator_id)

    await orchestrator_thread.create_thread()
    suggestion = await orchestrator_thread.process_message_and_await_response(
        user_input
    )
    return suggestion


async def process_with_psychologist(suggestion):
    psychologist_id = os.getenv("PSYCHOLOGIST_ASSISTANT_ID")
    psychologist_thread = AsyncThread(psychologist_id)

    await psychologist_thread.create_thread()
    psychology_result = await psychologist_thread.process_message_and_await_response(
        suggestion
    )
    return psychology_result


async def process_with_wardrobe(suggestion):
    wardrobe_id = os.getenv("WARDROBE_ASSISTANT_ID")
    wardrobe_thread = AsyncThread(wardrobe_id)

    await wardrobe_thread.create_thread()
    product_info = await wardrobe_thread.process_message_and_await_response(
        f"{suggestion}"
    )
    return product_info
