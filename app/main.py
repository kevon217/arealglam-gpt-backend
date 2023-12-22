import sys

sys.path.append("/app")
import json
import asyncio
import logging
from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from utils.websockets import ConnectionManager
from services.assistant_processing import (
    process_with_orchestrator,
    process_with_psychologist,
    extract_wardrobe_details,
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


# Simple HTTP GET Endpoint for Testing
@app.get("/ping")
async def ping():
    return {"message": "You are connected to A Real Glam' Fashion Adviser"}


# Run the app
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    logger.info("Connected to WebSocket")
    try:
        while True:
            # RECEIVE MESSAGE FROM CLIENT AND CONFIRM RECEIPT
            user_message = await websocket.receive_json()
            logger.info(user_message)
            await websocket.send_json(
                json.dumps(f"User Message Received: {user_message}")
            )

            # ORCHESTRATOR TASK
            async def wrapped_orchestrator_task():
                result = await process_with_orchestrator(user_message["message"])
                return ("orchestrator", result)

            orchestrator_task = asyncio.create_task(wrapped_orchestrator_task())
            task_map = {orchestrator_task: "orchestrator"}
            logger.info("Running process_with_orchestrator")
            _, orchestrator_result = await orchestrator_task
            initial_suggestion = orchestrator_result[
                0
            ]  # Get the first item from the list of results
            logger.info(f"Orchestrator response: {initial_suggestion}")
            await manager.send_personal_message(
                json.dumps({"orchestrator_suggestion": initial_suggestion}), websocket
            )

            logger.info("Initializing secondary agent tasks")

            # PSYCHOLOGIST TASK
            async def wrapped_psychologist_task():
                result = await process_with_psychologist(initial_suggestion)
                return ("psychologist", result)

            psychologist_task = asyncio.create_task(wrapped_psychologist_task())
            task_map[psychologist_task] = "psychologist"

            # WARDROBE TASKS
            wardrobe_details = await extract_wardrobe_details(initial_suggestion)
            for i, detail in enumerate(wardrobe_details, start=1):

                async def wrapped_wardrobe_task(detail, index):
                    result = await process_with_wardrobe(detail)
                    return (f"wardrobe_{index}", result)

                # Create task for each wardrobe item
                wardrobe_task = asyncio.create_task(wrapped_wardrobe_task(detail, i))
                task_map[wardrobe_task] = f"wardrobe_{i}"

            # PROCESS PSYCHOLOGIST & WARDROBE RETRIEVAL TASKS
            for completed_coroutine in asyncio.as_completed(task_map.keys()):
                task_type, completed_task_result = await completed_coroutine

                # Send message based on task type
                if task_type == "psychologist":
                    await manager.send_personal_message(
                        json.dumps({"psychologist_response": completed_task_result}),
                        websocket,
                    )
                elif task_type.startswith("wardrobe_"):
                    await manager.send_personal_message(
                        json.dumps({"wardrobe_retrieval": completed_task_result}),
                        websocket,
                    )

            logger.info("Finished processing secondary agents")

    except WebSocketDisconnect:
        await manager.disconnect(websocket)

    # finally:
    #     # Disconnect only if WebSocket is not already closed
    #     if not websocket.application_state == WebSocketState.DISCONNECTED:
    #         await manager.disconnect(client_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
