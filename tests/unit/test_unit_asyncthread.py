import unittest
from unittest.mock import patch, AsyncMock
from app.threads.async_thread import AsyncThread
from app.services import secondary_services
from services import assistant_processing


class TestAsyncThread(unittest.TestCase):
    @patch("openai.AsyncOpenAI", new_callable=AsyncMock)
    async def test_send_message(self, mock_openai):
        thread = AsyncThread("test_id")
        await thread.send_message("test_message")
        mock_openai.beta.threads.messages.create.assert_called_once()


class TestOrchestratorService(unittest.TestCase):
    @patch("app.services.orchestrator_service.AsyncThread", new_callable=AsyncMock)
    async def test_process_with_orchestrator(self, mock_thread):
        result = await assistant_processing.process_with_orchestrator("test_input")
        mock_thread.create_thread.assert_called_once()
        mock_thread.send_message.assert_called_once()
        mock_thread.await_response.assert_called_once()


class TestSecondaryServices(unittest.TestCase):
    @patch("app.services.secondary_services.AsyncThread", new_callable=AsyncMock)
    async def test_process_with_psychologist(self, mock_thread):
        result = await secondary_services.process_with_psychologist("test_suggestion")
        mock_thread.create_thread.assert_called_once()
        mock_thread.send_message.assert_called_once()
        mock_thread.await_response.assert_called_once()

    @patch("app.services.secondary_services.AsyncThread", new_callable=AsyncMock)
    async def test_process_with_wardrobe(self, mock_thread):
        result = await secondary_services.process_with_wardrobe(
            "test_suggestion", "test_input"
        )
        mock_thread.create_thread.assert_called_once()
        mock_thread.send_message.assert_called_once()
        mock_thread.await_response.assert_called_once()


if __name__ == "__main__":
    unittest.main()
