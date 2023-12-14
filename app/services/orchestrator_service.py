# orchestrator_service.py
import os
import asyncio
from dotenv import load_dotenv

from app.threads.async_thread import AsyncThread
from app.utils.assistants import get_assistant
from app.services.async_processing import process_secondary_agents

load_dotenv()


async def process_with_orchestrator(user_input):
    orchestrator_id = os.getenv("ORCHESTRATOR_ID")
    orchestrator_thread = AsyncThread(orchestrator_id)

    await orchestrator_thread.create_thread()
    await orchestrator_thread.send_message(user_input)
    suggestion = await orchestrator_thread.await_response()

    # Immediately return the suggestion and start secondary processing
    asyncio.create_task(process_secondary_agents(suggestion, user_input))
    return suggestion
