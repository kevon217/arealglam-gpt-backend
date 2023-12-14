import asyncio
from app.services.secondary_services import (
    process_with_psychologist,
    process_with_wardrobe,
)


async def process_secondary_agents(suggestion, user_input, thread):
    psychology_result, product_info = await asyncio.gather(
        process_with_psychologist(suggestion, thread),
        process_with_wardrobe(suggestion, user_input, thread),
    )

    # Logic to send secondary results to frontend (via WebSocket or other means)
    # ...
