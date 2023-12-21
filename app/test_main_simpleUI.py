import sys

sys.path.append("/app")
import json
import asyncio
import logging
from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse  # for testing
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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
app.mount(
    "/static", StaticFiles(directory="static"), name="static"
)  # for testing with simple ui
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


@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


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
            data = await websocket.receive_json()
            logger.info(data)
            await websocket.send_json(json.dumps("User Message Received"))

            # Send the message to the orchestrator
            logger.info("Running process_with_orchestrator")
            initial_suggestion = await process_with_orchestrator(data["message"])
            print(initial_suggestion)
            logger.info(f"Orchestrator response: {initial_suggestion}")
            await manager.send_personal_message(
                json.dumps({"fashion_suggestion": initial_suggestion}), websocket
            )

            logger.info("Initializing secondary agent tasks")

            # Wrapper function for psychologist task
            async def wrapped_psychologist_task():
                result = await process_with_psychologist(initial_suggestion)
                return ("psychologist", result)

            psychologist_task = asyncio.create_task(wrapped_psychologist_task())

            # Extract wardrobe details and initialize tasks for each detail
            wardrobe_details = await extract_wardrobe_details(initial_suggestion)

            # Wrapper function for each wardrobe task
            async def wrapped_wardrobe_task(wardrobe_details):
                result = await process_with_wardrobe(wardrobe_details)
                return ("wardrobe", result)

            wardrobe_tasks = [
                asyncio.create_task(wrapped_wardrobe_task(product))
                for product in wardrobe_details
            ]

            # Combine all tasks into one list
            all_tasks = [psychologist_task] + wardrobe_tasks

            # Process tasks as they complete
            for completed_coroutine in asyncio.as_completed(all_tasks):
                task_type, completed_task_result = await completed_coroutine

                # Send message based on task type
                if task_type == "psychologist":
                    await manager.send_personal_message(
                        json.dumps({"psychologist_response": completed_task_result[0]}),
                        websocket,
                    )
                elif task_type == "wardrobe":
                    await manager.send_personal_message(
                        json.dumps({"wardrobe_retrieval": completed_task_result}),
                        websocket,
                    )

            logger.info("Finished processing secondary agents")

    except WebSocketDisconnect:
        await manager.disconnect(websocket)

    # TO DO:
    # finally:
    #     # Disconnect only if WebSocket is not already closed
    #     if not websocket.application_state == WebSocketState.DISCONNECTED:
    #         await manager.disconnect(client_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
