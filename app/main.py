from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import asyncio

from app.services.orchestrator_service import process_with_orchestrator
from app.services.async_processing import process_secondary_agents
from app.threads.async_thread import AsyncThread

app = FastAPI()


# Define the data model for incoming queries
class Query(BaseModel):
    user_input: str


# Websocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Future logic to handle real-time communication
        await websocket.send_text(f"Received: {data}")


# Endpoint to handle user queries
@app.post("/query")
async def handle_query(query: Query):
    # Process query with orchestrator agent
    initial_suggestion = await process_with_orchestrator(query.user_input)

    # Send initial suggestion back to frontend via WebSocket or similar
    await send_realtime_update("initial_suggestion", initial_suggestion)

    # Concurrently process secondary agents
    asyncio.create_task(process_secondary_agents(initial_suggestion, query.user_input))

    return {"status": "Processing"}


# Function to send real-time updates to the frontend
async def send_realtime_update(message_type, data):
    # Logic to send updates via WebSocket or similar
    # This will be integrated with the WebSocket connection once established
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
