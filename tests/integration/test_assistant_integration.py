import os
import unittest
import asyncio
from dotenv import load_dotenv

load_dotenv()

from app.threads.async_thread import AsyncThread


class TestAssistantIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_assistant_workflow(self):
        # Define the user message
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

        # Send message to the orchestrator and receive fashion suggestion
        fashion_suggestion = (
            await orchestrator_thread.process_message_and_await_response(user_message)
        )
        print(f"Orchestrator Suggestion: {fashion_suggestion}")

        # Orchestrator sends messages to Psychologist and Wardrobe assistants
        await psychologist_thread.send_message_to_thread(
            fashion_suggestion + " " + user_message
        )
        await wardrobe_thread.send_message_to_thread(
            fashion_suggestion + " " + user_message
        )

        # Create runs and await responses from secondary assistants
        psychologist_response = (
            await psychologist_thread.process_message_and_await_response(user_message)
        )
        wardrobe_response = await wardrobe_thread.process_message_and_await_response(
            user_message
        )

        # Output secondary assistants' responses
        print(f"Psychologist Response: {psychologist_response}")
        print(f"Wardrobe Response: {wardrobe_response}")

        # Optional: Orchestrator receives responses from secondary assistants
        # This part is currently not implemented as per the requirement

        # Assertions to ensure valid responses (optional)
        self.assertIsNotNone(fashion_suggestion)
        self.assertIsNotNone(psychologist_response)
        self.assertIsNotNone(wardrobe_response)


if __name__ == "__main__":
    unittest.main(exit=False)
