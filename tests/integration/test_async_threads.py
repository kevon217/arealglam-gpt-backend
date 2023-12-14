import os
import unittest
import asyncio
from dotenv import load_dotenv

load_dotenv()

from app.threads.async_thread import AsyncThread


class TestAsyncThreadIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_send_message(self):
        assistant_ids = [
            os.getenv("ORCHESTRATOR_ASSISTANT_ID"),
            os.getenv("PSYCHOLOGIST_ASSISTANT_ID"),
            os.getenv("WARDROBE_ASSISTANT_ID"),
        ]
        user_message = (
            "Your Perfect First Date Ensemble: Trendy, Charming, and Confident..."
        )

        tasks = [
            self.send_and_await_message(assistant_id, user_message)
            for assistant_id in assistant_ids
        ]
        for task in asyncio.as_completed(tasks):
            response, assistant_id = await task
            print(f"Response from assistant {assistant_id}: {response}")
            self.assertIsNotNone(response)

    async def send_and_await_message(self, assistant_id, message):
        print(f"Processing assistant with ID: {assistant_id}")
        thread = AsyncThread(assistant_id)
        await thread.create_thread()
        response = await thread.process_message_and_await_response(message)
        return response, assistant_id


if __name__ == "__main__":
    unittest.main(exit=False)
