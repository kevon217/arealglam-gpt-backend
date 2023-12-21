import asyncio
from app.services.assistant_processing import (
    process_with_orchestrator,
    process_with_psychologist,
    process_with_wardrobe,
)  # import your actual functions


async def test_async_logic(user_input):
    # Simulate receiving a message
    initial_suggestion = await process_with_orchestrator(user_input)
    print(f"Orchestrator response: {initial_suggestion[0]}")

    # Initializing secondary agent tasks
    psychologist_task = asyncio.create_task(
        process_with_psychologist(initial_suggestion)
    )

    # Map secondary tasks to identifiers
    task_map = {
        psychologist_task: "psychologist",
    }

    # Iterate over the tasks as they complete
    for completed_coroutine in asyncio.as_completed([psychologist_task]):
        completed_task_result = await completed_coroutine

        # Find which task has completed
        for task, identifier in task_map.items():
            if task.done():
                if identifier == "psychologist":
                    print(f"Psychologist response: {completed_task_result[0]}")
                break

    print("Finished processing secondary agents")

    # Simulate wardrobe retrieval response (if needed)
    simulated_wardrobe_response = {"products": [43, 35, 39]}
    return simulated_wardrobe_response


# Example usage
if __name__ == "__main__":
    user_input = "What should I wear for a cold summer beach party?"
    asyncio.run(test_async_logic(user_input=user_input))
