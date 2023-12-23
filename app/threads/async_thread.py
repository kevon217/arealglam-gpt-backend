import asyncio
import json
import logging
from colorlog import ColoredFormatter
import openai
from utils.oai_clients import get_openai_async_client


class AsyncThread:
    def __init__(self, assistant_id):
        self.assistant_id = assistant_id
        self.client = get_openai_async_client()
        self.function_calls = []  # Store function calls for processing
        self.format_wardrobe_response_handled = (
            False  # Flag to track special processing
        )
        # Use the centralized logger
        self.logger = logging.getLogger("ARealGlamApp.async_thread")
        self.logger.propagate = (
            True  # Prevent logging messages from propagating to the root logger
        )

    async def create_thread(self):
        self.thread = await self.client.beta.threads.create()
        self.thread_id = self.thread.id
        self.logger.info(f"Thread created with ID: {self.thread_id}")

    async def send_message_to_thread(self, message):
        # Ensure message is a string
        if not isinstance(message, str):
            if isinstance(message, list):
                message = " ".join(message)
            else:
                message = json.dumps(message)

        response = await self.client.beta.threads.messages.create(
            thread_id=self.thread_id, role="user", content=message
        )
        self.logger.info(f"Message sent to thread {self.thread_id}: {message}")

    async def create_run_for_thread(self):
        self.run = await self.client.beta.threads.runs.create(
            thread_id=self.thread_id, assistant_id=self.assistant_id
        )
        self.logger.info(f"Run created with ID: {self.run.id}")

    async def retrieve_run_status(self):
        self.run = await self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id, run_id=self.run.id
        )
        return self.run.status

    async def list_run_steps(self):
        return await self.client.beta.threads.runs.list_steps(
            thread_id=self.thread_id, run_id=self.run.id
        )

    async def submit_tool_outputs_and_retrieve(self, tool_outputs):
        await self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread_id, run_id=self.run.id, tool_outputs=tool_outputs
        )
        return await self.retrieve_run_status()

    async def await_run_completion(self):
        all_results = []
        while True:
            status = await self.retrieve_run_status()
            if status in ["completed", "failed", "cancelled", "expired"]:
                if status == "completed":
                    self.logger.info(f"Run {self.run.id} completed successfully")
                    result = await self.get_latest_assistant_message()
                    all_results.append(result)
                break
            elif status == "requires_action":
                if not self.format_wardrobe_response_handled:
                    (
                        tool_outputs,
                        continue_standard_process,
                    ) = await self.custom_function_handler()
                    if continue_standard_process:
                        await self.submit_tool_outputs_and_retrieve(tool_outputs)
                    else:
                        all_results.extend(tool_outputs)
                        self.format_wardrobe_response_handled = True
                else:
                    break
            # await asyncio.sleep(1)
        return all_results

    async def custom_function_handler(self):
        tool_calls = self.run.required_action.submit_tool_outputs.tool_calls
        processed_outputs = []
        continue_standard_process = True

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if (
                function_name == "format_wardrobe_response"
                or function_name == "format_empty_wardrobe_response"
            ):
                # Custom processing for 'format_wardrobe_response' and 'format_empty_wardrobe_response'
                json_result = self.parse_json_from_arguments(arguments)
                processed_outputs.append(json_result)
                continue_standard_process = False
            else:
                # Standard processing for other function calls
                reformatted_query = self.reformat_for_search(function_name, arguments)
                tool_output = {
                    "tool_call_id": tool_call.id,
                    "output": reformatted_query,
                }
                processed_outputs.append(tool_output)

        return processed_outputs, continue_standard_process

    def parse_json_from_arguments(self, arguments):
        # Return the arguments directly as they are already in dictionary form
        return arguments

    async def get_latest_assistant_message(self):
        # Retrieve the latest assistant message after the run has completed
        messages = await self.client.beta.threads.messages.list(
            thread_id=self.thread_id
        )
        for message in reversed(messages.data):
            if (
                message.role == "assistant"
                and message.assistant_id == self.assistant_id
            ):
                # Iterating through the content list to find the text value
                for content_item in message.content:
                    if content_item.type == "text":
                        return content_item.text.value
        return None

    async def process_function_calls(self):
        tool_calls = self.run.required_action.submit_tool_outputs.tool_calls
        self.logger.info(f"Processing function calls: {len(tool_calls)} calls found")
        tool_outputs = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            reformatted_query = self.reformat_for_search(function_name, arguments)
            tool_output = {"tool_call_id": tool_call.id, "output": reformatted_query}
            tool_outputs.append(tool_output)
            self.logger.info(
                f"Prepared tool output for {function_name}: {reformatted_query}"
            )
        return tool_outputs

    def reformat_for_search(self, function_name, arguments):
        # Logic to transform arguments into a search query for the knowledge base
        description = arguments.get("description", "")
        search_instruction = f"Please use the retrieval tool to search our knowledge base for products matching the description: '{description}'."
        return search_instruction

    async def submit_reformatted_query(self, tool_outputs):
        await self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread_id, run_id=self.run.id, tool_outputs=tool_outputs
        )

    async def process_message_and_await_response(self, message):
        self.logger.info("Processing message and awaiting response...")
        self.format_wardrobe_response_handled = False  # Reset flag for new processing
        await self.send_message_to_thread(message)
        await self.create_run_for_thread()
        return await self.await_run_completion()

    # async def process_message_annotations(self, message):
    #     for annotation in message.annotations:
    #         if annotation.type == "file_citation":
    #             citation_detail = f"{annotation.file_citation.quote} from {annotation.file_citation.file_id}"
    #             message.content = message.content.replace(annotation.text, citation_detail)
    #         elif annotation.type == "file_path":
    #             file_path_detail = f"File at {annotation.file_path.file_id}"
    #             message.content = message.content.replace(annotation.text, file_path_detail)
    #     return message.content
