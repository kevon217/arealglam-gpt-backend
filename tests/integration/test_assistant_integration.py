import os
import unittest
import asyncio
import time
from dotenv import load_dotenv

load_dotenv()

from app.threads.async_thread import AsyncThread


class TestAssistantIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_assistant_workflow(self):
        user_message = "What should I wear for a summer beach party?"

        # Define assistant IDs
        orchestrator_id = os.getenv("ORCHESTRATOR_ASSISTANT_ID")
        psychologist_id = os.getenv("PSYCHOLOGIST_ASSISTANT_ID")
        wardrobe_id = os.getenv("WARDROBE_ASSISTANT_ID")

        # Create threads for each assistant
        orchestrator_thread = AsyncThread(orchestrator_id)
        psychologist_thread = AsyncThread(psychologist_id)
        wardrobe_thread = AsyncThread(wardrobe_id)

        # Initialize threads
        await orchestrator_thread.create_thread()
        await psychologist_thread.create_thread()
        await wardrobe_thread.create_thread()

        # Start time for orchestrator
        start_time_orchestrator = time.time()

        # Send message to the orchestrator and receive fashion suggestion
        fashion_suggestion = (
            await orchestrator_thread.process_message_and_await_response(user_message)
        )
        end_time_orchestrator = time.time()
        print(
            f"Orchestrator Suggestion: {fashion_suggestion} (Time Taken: {end_time_orchestrator - start_time_orchestrator:.2f} seconds)"
        )

        # Create tasks for secondary assistants
        psychologist_task = asyncio.create_task(
            self.assistant_task(
                psychologist_thread,
                fashion_suggestion + " " + user_message,
                "Psychologist",
            )
        )
        wardrobe_task = asyncio.create_task(
            self.assistant_task(
                wardrobe_thread, fashion_suggestion + " " + user_message, "Wardrobe"
            )
        )

        # Use asyncio.as_completed to process tasks as they are completed
        for future in asyncio.as_completed([psychologist_task, wardrobe_task]):
            assistant_name, response, time_taken = await future
            print(
                f"{assistant_name} Response: {response} (Time Taken: {time_taken:.2f} seconds)"
            )

        # Assertions to ensure valid responses
        self.assertIsNotNone(fashion_suggestion)
        self.assertTrue(any([psychologist_task.done(), wardrobe_task.done()]))

    async def assistant_task(self, thread, message, assistant_name):
        start_time = time.time()
        response = await thread.process_message_and_await_response(message)
        end_time = time.time()
        return assistant_name, response, end_time - start_time


if __name__ == "__main__":
    unittest.main(exit=False)
