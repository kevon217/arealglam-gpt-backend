import asyncio
from app.utils.oai_client_async import get_openai_client


class AsyncThread:
    def __init__(self, assistant_id):
        self.assistant_id = assistant_id
        self.client = get_openai_client()

    async def create_thread(self):
        self.thread = await self.client.beta.threads.create()
        self.thread_id = self.thread.id
        print(f"Thread created with ID: {self.thread_id}")

    async def send_message_to_thread(self, message):
        await self.client.beta.threads.messages.create(
            thread_id=self.thread_id, role="user", content=message
        )
        print(f"Message sent to thread {self.thread_id}.")

    async def create_run_for_thread(self):
        self.run = await self.client.beta.threads.runs.create(
            thread_id=self.thread_id, assistant_id=self.assistant_id
        )
        print(f"Run created with ID: {self.run.id}")

    async def await_run_completion(self):
        while True:
            self.run = await self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id, run_id=self.run.id
            )
            print(f"Checking run status: {self.run.status}")
            if self.run.status in [
                "completed",
                "failed",
                "cancelled",
                "cancelling",
                "expired",
            ]:
                break
            await asyncio.sleep(1)

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
                for content in message.content:
                    if content["type"] == "text":
                        return content["text"]["value"]
        return None

    async def process_message_and_await_response(self, message):
        await self.send_message_to_thread(message)
        await self.create_run_for_thread()
        await self.await_run_completion()
        response = await self.get_latest_assistant_message()
        return response
