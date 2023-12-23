import os
import asyncio
import logging
import json
from dotenv import load_dotenv
from utils.oai_clients import client_async
from utils.logging_setup import setup_logging
from threads.async_thread import AsyncThread
from assistants.function_calls.wardrobe_functions import wardrobe_tools

# from app.utils.assistants import get_assistant

load_dotenv()

# Use the centralized logger
logger = logging.getLogger("ARealGlamApp.async_thread")
logger.propagate = True  # Prevent logging messages from propagating to the root logger


async def process_with_orchestrator(user_input):
    """
    Process user input with the orchestrator assistant.
    """
    logger.info("Processing with Orchestrator")
    orchestrator_id = os.getenv("ORCHESTRATOR_ASSISTANT_ID")
    orchestrator_thread = AsyncThread(orchestrator_id)

    await orchestrator_thread.create_thread()
    initial_response = await orchestrator_thread.process_message_and_await_response(
        user_input
    )
    logger.info(f"Orchestrator's raw initial response: {initial_response}")
    return initial_response


async def process_with_psychologist(suggestion):
    """
    Process the suggestion with the psychologist assistant.
    """
    logger.info("Processing with Psychologist")
    psychologist_id = os.getenv("PSYCHOLOGIST_ASSISTANT_ID")
    psychologist_thread = AsyncThread(psychologist_id)

    await psychologist_thread.create_thread()
    psychologist_response = (
        await psychologist_thread.process_message_and_await_response(suggestion)
    )
    logger.info(f"Psychologist's response: {psychologist_response}")
    return psychologist_response


def parse_tool_call_outputs(tool_calls):
    """
    Parse the tool call outputs into a list of categories, each containing its descriptions.
    """
    category_lists = []
    for tool_call in tool_calls:
        wardrobe_items = json.loads(tool_call.function.arguments).get(
            "wardrobe_items", {}
        )
        # Iterate over each category in wardrobe_items
        for category, items in wardrobe_items.items():
            if items:  # Check if the category has items
                category_lists.append(
                    items
                )  # Append the list of items for this category

    # NOTE: may want to consider separate searches for multiple items in a single category list
    return category_lists


async def extract_wardrobe_items(suggestion):
    """
    Extract the wardrobe details from the suggestion.
    """
    logger.info("Extracting wardrobe details")
    messages = [
        {
            "role": "user",
            "content": f"From the fashion suggestion '{suggestion}', use parallel function calls to extract each distinct wardrobe item. Use the specific function calls for tops, bottoms, jackets, shoes, and accessories as applicable. If there are multiple distinct options for a single type of product, such as 'floaty kaftan or a breezy linen shirt', apply the function calls separately for each option. The response should clearly list each item with its key features, for example, 'floaty kaftan', 'breezy linen shirt', 'comfortable shorts', 'strappy sandals', without additional advice or commentary. Aim for a concise and direct list of items and their descriptors.",
        }
    ]
    response = await client_async.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=wardrobe_tools,
        tool_choice={
            "type": "function",
            "function": {"name": "extract_wardrobe_items"},
        },  # auto is default, but we'll be explicit
    )
    tool_calls = response.choices[0].message.tool_calls
    wardrobe_items = parse_tool_call_outputs(tool_calls)
    return wardrobe_items


async def process_with_wardrobe(wardrobe_items):
    """
    Process a single wardrobe item description with the wardrobe assistant.
    """
    logger.info(f"Retrieving product IDs for: {wardrobe_items}")
    wardrobe_id = os.getenv("WARDROBE_ASSISTANT_ID")
    wardrobe_thread = AsyncThread(wardrobe_id)

    await wardrobe_thread.create_thread()
    product_ids = await wardrobe_thread.process_message_and_await_response(
        wardrobe_items
    )
    logger.info(f"Wardrobe retrieved product IDs for '{wardrobe_items}': {product_ids}")

    return product_ids
