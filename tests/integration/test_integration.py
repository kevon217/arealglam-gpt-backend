import os
import unittest
import asyncio
import time
import yaml
from datetime import datetime
import shutil
from pathlib import Path

from app.threads.async_thread import AsyncThread
from dotenv import load_dotenv

load_dotenv()


class TestAssistantIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_assistant_workflow(self):
        # Load test configuration from YAML file
        with open("tests/integration/config.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)

        # Extract user message and assistant IDs from config
        user_message = config["tests"]["user_message"][0]
        orchestrator_id = os.getenv("ORCHESTRATOR_ASSISTANT_ID")
        psychologist_id = os.getenv("PSYCHOLOGIST_ASSISTANT_ID")
        wardrobe_id = os.getenv("WARDROBE_ASSISTANT_ID")

        # Create threads for each assistant
        orchestrator_thread = AsyncThread(orchestrator_id)
        # wardrobe_thread = AsyncThread(wardrobe_id)
        psychologist_thread = AsyncThread(psychologist_id)

        # Initialize threads
        await orchestrator_thread.create_thread()
        # await wardrobe_thread.create_thread()
        await psychologist_thread.create_thread()

        # Conduct test and log results
        # results = await self.conduct_test(orchestrator_thread, wardrobe_thread, psychologist_thread, user_message)
        results = await self.conduct_test(
            orchestrator_thread, psychologist_thread, user_message
        )

        # Save results to output folder
        self.save_results(results, config)

    # async def conduct_test(self, orchestrator_thread, wardrobe_thread, psychologist_thread, user_message):
    async def conduct_test(
        self, orchestrator_thread, psychologist_thread, user_message
    ):
        start_time_orchestrator = time.time()
        fashion_suggestion = (
            await orchestrator_thread.process_message_and_await_response(user_message)
        )
        end_time_orchestrator = time.time()

        fashion_suggestion = fashion_suggestion[
            -1
        ]  # Assuming the relevant message is the last item

        # Responses and timings
        results = {
            "orchestrator": {
                "response": fashion_suggestion,
                "time_taken": end_time_orchestrator - start_time_orchestrator,
            }
        }

        # Secondary assistants

        # wardrobe_task = asyncio.create_task(
        #     self.assistant_task(wardrobe_thread, fashion_suggestion, "Wardrobe")
        # )
        psychologist_task = asyncio.create_task(
            self.assistant_task(psychologist_thread, fashion_suggestion, "Psychologist")
        )

        for future in asyncio.as_completed([psychologist_task]):
            assistant_name, response, time_taken = await future
            results[assistant_name.lower()] = {
                "response": response,
                "time_taken": time_taken,
            }

        return results
        # for future in asyncio.as_completed([psychologist_task, wardrobe_task]):
        #     assistant_name, response, time_taken = await future
        #     results[assistant_name.lower()] = {
        #         "response": response,
        #         "time_taken": time_taken
        #     }

        # return results

    async def assistant_task(self, thread, message, assistant_name):
        start_time = time.time()
        response = await thread.process_message_and_await_response(message)
        end_time = time.time()
        return assistant_name, response, end_time - start_time

    def save_results(self, results, config):
        # Create output folder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(f"tests/output/{timestamp}")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save results to a file
        with open(output_dir / "results.txt", "w") as file:
            for assistant, data in results.items():
                file.write(
                    f"{assistant.capitalize()} Response: {data['response']} (Time Taken: {data['time_taken']:.2f} seconds)\n"
                )

        # Copy YAML config to output folder
        config_file_path = "tests/integration/config.yaml"
        shutil.copy(config_file_path, output_dir / "config.yaml")

        # Copy log file to output folder
        log_file_path = "async_thread.log"
        if os.path.exists(log_file_path):
            shutil.copy(log_file_path, output_dir / "async_thread.log")
        else:
            print("Log file not found.")


if __name__ == "__main__":
    unittest.main(exit=False)
