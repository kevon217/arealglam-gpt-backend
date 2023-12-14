# app/routers/query_router.py
from fastapi import APIRouter, WebSocket
import asyncio
from app.services import orchestrator_service, async_processing

query_router = APIRouter()


@query_router.post("/query")
async def handle_query(user_input: str):
    # Process with Orchestrator and immediately return initial suggestion
    initial_suggestion = await orchestrator_service.process_with_orchestrator(
        user_input
    )

    # Start secondary processing
    asyncio.create_task(
        async_processing.process_secondary_agents(initial_suggestion, user_input)
    )

    return {"initial_suggestion": initial_suggestion}


@query_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # WebSocket logic for real-time communication
