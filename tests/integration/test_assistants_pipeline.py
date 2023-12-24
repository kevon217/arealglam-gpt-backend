import asyncio
import time
import unittest
from datetime import datetime
from pathlib import Path
import shutil
import yaml
import os
import json
from app.threads.async_thread import AsyncThread
from app.services.assistant_processing import (
    process_with_orchestrator,
    process_with_psychologist,
    process_with_wardrobe,
    extract_wardrobe_items,
)


class TestAssistantsPipeline(unittest.IsolatedAsyncioTestCase):
    async def test_assistant_workflow(self):
        # Load test configuration from YAML file
        with open("tests/integration/config.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)

        # Extract user message and assistant IDs from config
        user_message = config["tests"]["user_message"][0]

        # Wrapper function for orchestrator task
        async def wrapped_orchestrator_task():
            result = await process_with_orchestrator(user_message)
            return ("orchestrator", result)

        orchestrator_task = asyncio.create_task(wrapped_orchestrator_task())

        # Initialize a dictionary to map task to its identifier
        task_map = {orchestrator_task: "orchestrator"}

        # Process the orchestrator task first to get the suggestion
        _, orchestrator_result = await orchestrator_task
        initial_suggestion = orchestrator_result[
            0
        ]  # Get the first item from the list of results

        if initial_suggestion.endswith("[FASHION_OK]"):
            proceed = True
            fashion_suggestion = initial_suggestion.replace("[FASHION_OK]", "").strip()
        elif initial_suggestion.endswith("[FASHION_WAIT]"):
            proceed = False
        else:
            proceed = False  # Default action if no keyword is found
            print(
                "Issue with Orchestrator assistant not ending with appropriate keyword."
            )

        # Wrapper function for psychologist task
        async def wrapped_psychologist_task():
            result = await process_with_psychologist(initial_suggestion)
            return ("psychologist", result)

        psychologist_task = asyncio.create_task(wrapped_psychologist_task())
        task_map[psychologist_task] = "psychologist"

        # Extract wardrobe details and initialize tasks for each detail
        wardrobe_items = await extract_wardrobe_items(initial_suggestion)

        # Wrapper function for each wardrobe task with unique identifier
        for i, item in enumerate(wardrobe_items, start=1):

            async def wrapped_wardrobe_task(item, index):
                result = await process_with_wardrobe(item)
                return (f"wardrobe_{index}", result)

            wardrobe_task = asyncio.create_task(wrapped_wardrobe_task(item, i))
            task_map[wardrobe_task] = f"wardrobe_{i}"

        # Process tasks as they complete and store results
        results = {}
        for completed_coroutine in asyncio.as_completed(task_map.keys()):
            task_type, completed_task_result = await completed_coroutine
            results[task_type] = completed_task_result

        # Test assertions and/or result logging
        for key in task_map.values():
            self.assertIn(key, results)

        # Save results and log
        self.save_results(results, config)

    def save_results(self, results, config):
        # Create output folder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(f"tests/output/{timestamp}")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save results to a file
        with open(output_dir / "results.txt", "w") as file:
            for assistant_type, response in results.items():
                file.write(
                    f"{assistant_type.capitalize()} Response: {json.dumps(response, indent=2)}\n"
                )

        # Copy YAML config to output folder
        config_file_path = "tests/pipeline/config.yaml"
        shutil.copy(config_file_path, output_dir / "config.yaml")

        # Copy log file to output folder
        log_file_path = "async_thread.log"
        if os.path.exists(log_file_path):
            shutil.copy(log_file_path, output_dir / "async_thread.log")
        else:
            print("Log file not found.")


if __name__ == "__main__":
    import sys

    sys.path.append("/app")
    unittest.main(exit=False)
