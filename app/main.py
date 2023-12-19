import json
import asyncio
import logging
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.utils.websockets import ConnectionManager
from app.services.assistant_processing import (
    process_with_orchestrator,
    process_with_psychologist,
    process_with_wardrobe,
)


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

# Create FastAPI app
app = FastAPI()
manager = ConnectionManager()

# Set up CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Define Pydantic models
# class Query(BaseModel):
#     user_input: str
#     client_id: str  # Added to identify the user's WebSocket session


# Run the app
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(data)
            await websocket.send_json(json.dumps(data))

            # Send the message to the orchestrator
            logger.info("Running process_with_orchestrator")
            initial_suggestion = await process_with_orchestrator(data["message"])
            logger.info(f"Orchestrator response: {initial_suggestion[0]}")
            await manager.send_personal_message(
                f"initial_suggestion: {initial_suggestion[0]}", websocket
            )

            # Run the secondary agents in parallel
            logger.info("Initializing secondary agent tasks")
            psychologist_task = asyncio.create_task(
                process_with_psychologist(initial_suggestion)
            )
            wardrobe_task = asyncio.create_task(
                process_with_wardrobe(initial_suggestion)
            )

            # Use a regular for loop with asyncio.as_completed
            for task in asyncio.as_completed([psychologist_task, wardrobe_task]):
                result = await task
                if task == psychologist_task:
                    await manager.send_personal_message(
                        f"psychologist_response: {result}", websocket
                    )
                elif task == wardrobe_task:
                    await manager.send_personal_message(
                        f"wardrobe_retrieval: {json.dumps(result)}", websocket
                    )

            logger.info("Finished processing secondary agents")

    except WebSocketDisconnect:
        await manager.disconnect(websocket)

    # TO DO: NOT YET IMPLEMENTED!
    # finally:
    #     # Disconnect only if WebSocket is not already closed
    #     if not websocket.application_state == WebSocketState.DISCONNECTED:
    #         await manager.disconnect(client_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
