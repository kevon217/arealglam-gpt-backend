import json
import asyncio
import logging
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse  # for testing

import sys

sys.path.append("/app")


from utils.websockets import ConnectionManager
from services.assistant_processing import (
    process_with_orchestrator,
    process_with_psychologist,
    process_with_wardrobe,
)


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)


# # Define Pydantic models
# class Query(BaseModel):
#     user_input: str
#     client_id: str  # Added to identify the user's WebSocket session


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
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<html><body><h1>Welcome to the FastAPI Server</h1></body></html>"


# Run the app
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    logger.info("Connected to WebSocket")
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
                json.dumps({"fashion_suggestion": initial_suggestion[0]}), websocket
            )

            logger.info("Initializing secondary agent tasks")
            psychologist_task = asyncio.create_task(
                process_with_psychologist(initial_suggestion)
            )
            # wardrobe_task = asyncio.create_task(process_with_wardrobe(initial_suggestion))

            # Map secondary tasks to identifiers
            task_map = {
                psychologist_task: "psychologist",
                # wardrobe_task: 'wardrobe'
            }

            # Iterate over the tasks as they complete
            # for completed_coroutine in asyncio.as_completed([psychologist_task, wardrobe_task]):
            for completed_coroutine in asyncio.as_completed([psychologist_task]):
                completed_task_result = (
                    await completed_coroutine
                )  # Get the result of the completed task

                # Find which task has completed
                for task, identifier in task_map.items():
                    if task.done():
                        if identifier == "psychologist":
                            await manager.send_personal_message(
                                json.dumps(
                                    {"psychologist_response": completed_task_result[0]}
                                ),
                                websocket,
                            )
                        # elif identifier == 'wardrobe':
                        #     await manager.send_personal_message(f"wardrobe_retrieval: {json.dumps(completed_task_result)}", websocket)
                        break  # Exit the inner loop after finding the completed task

            logger.info("Finished processing secondary agents")

            # Simulate wardrobe retrieval response
            simulated_wardrobe_response = {"products": [43, 35, 39]}
            await manager.send_personal_message(
                f"wardrobe_retrieval: {json.dumps(simulated_wardrobe_response)}",
                websocket,
            )

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
    # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) # for testing
