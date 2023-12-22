import os
import asyncio
import logging
import json
from dotenv import load_dotenv
from utils.oai_clients import client_async
from threads.async_thread import AsyncThread
from assistants.function_calls.wardrobe_functions import wardrobe_tools

# from app.utils.assistants import get_assistant

load_dotenv()

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)


async def process_with_orchestrator(user_input):
    """
    Process user input with the orchestrator assistant.
    """
    logger.info("Processing with Orchestrator")
    orchestrator_id = os.getenv("ORCHESTRATOR_ASSISTANT_ID")
    orchestrator_thread = AsyncThread(orchestrator_id)

    await orchestrator_thread.create_thread()
    suggestion = await orchestrator_thread.process_message_and_await_response(
        user_input
    )
    logger.info(f"Orchestrator suggestion: {suggestion}")
    return suggestion


async def process_with_psychologist(suggestion):
    """
    Process the suggestion with the psychologist assistant.
    """
    logger.info("Processing with Psychologist")
    psychologist_id = os.getenv("PSYCHOLOGIST_ASSISTANT_ID")
    psychologist_thread = AsyncThread(psychologist_id)

    await psychologist_thread.create_thread()
    psychology_result = await psychologist_thread.process_message_and_await_response(
        suggestion
    )
    logger.info(f"Psychologist result: {psychology_result}")
    return psychology_result


def parse_tool_call_outputs(tool_calls):
    """
    Parse the tool call outputs into a list of descriptions.
    """
    descriptions = []
    for tool_call in tool_calls:
        # Assuming the output is in the form of {"description": "..."}
        description = json.loads(tool_call.function.arguments).get("description")
        if description:
            descriptions.append(description)
    return descriptions


async def extract_wardrobe_details(suggestion):
    """
    Extract the wardrobe details from the suggestion.
    """
    logger.info("Extracting wardrobe details")
    messages = [
        {
            "role": "user",
            "content": f"Extract unique wardrobe items from this fashion suggestion, while considering variations and avoiding duplication of items: {suggestion}. Use parallel function calls for tops, bottoms, jackets, shoes, and accessories. You do not need to call a particular function if the item associated with that function is not present in the fashion suggestion text. Remember, do not repeat function calls on the same item or call a specific function if the item isn't mentioned.",
        }
    ]
    response = await client_async.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=wardrobe_tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    tool_calls = response.choices[0].message.tool_calls
    wardrobe_details = parse_tool_call_outputs(tool_calls)
    return wardrobe_details


async def process_with_wardrobe(wardrobe_details):
    """
    Process a single wardrobe item description with the wardrobe assistant.
    """
    logger.info(f"Retrieving product IDs for: {wardrobe_details}")
    wardrobe_id = os.getenv("WARDROBE_ASSISTANT_ID")
    wardrobe_thread = AsyncThread(wardrobe_id)

    await wardrobe_thread.create_thread()
    product_ids = await wardrobe_thread.process_message_and_await_response(
        wardrobe_details
    )
    logger.info(f"Retrieved product IDs for '{wardrobe_details}': {product_ids}")

    return product_ids
