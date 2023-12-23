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
from utils.logging_setup import setup_logging
from services.assistant_processing import (
    process_with_orchestrator,
    process_with_psychologist,
    extract_wardrobe_items,
    process_with_wardrobe,
)

# Create logger
logger = setup_logging()

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
            initial_response = orchestrator_result[0]

            # DECIDE WHETHER TO PROCEED WITH SECONDARY AGENTS
            if initial_response.endswith("[FASHION_OK]"):
                proceed = True
                fashion_suggestion = initial_response.replace(
                    "[FASHION_OK]", ""
                ).strip()
                await manager.send_personal_message(
                    json.dumps({"orchestrator_suggestion": fashion_suggestion}),
                    websocket,
                )
            elif initial_response.endswith("[FASHION_WAIT]"):
                proceed = False
                normal_reply = initial_response.replace("[FASHION_WAIT]", "").strip()
                await manager.send_personal_message(
                    json.dumps({"orchestrator_reply": normal_reply}), websocket
                )
            else:
                proceed = False  # Default action if no keyword is found
                logging.debug(
                    "Issue with Orchestrator assistant not ending with appropriate keyword."
                )

            if proceed:
                logger.info("Initializing secondary agent tasks")

                # PSYCHOLOGIST TASK
                async def wrapped_psychologist_task():
                    psychologist_response = await process_with_psychologist(
                        fashion_suggestion
                    )  # TODO: ADD USER'S MESSAGE TO PSYCHOLOGIST TASK AS WELL
                    return ("psychologist", psychologist_response)

                psychologist_task = asyncio.create_task(wrapped_psychologist_task())
                task_map[psychologist_task] = "psychologist"

                # WARDROBE TASKS
                wardrobe_items = await extract_wardrobe_items(fashion_suggestion)
                for i, item in enumerate(wardrobe_items, start=1):

                    async def wrapped_wardrobe_task(item, index):
                        product_ids = await process_with_wardrobe(item)
                        return (f"wardrobe_{index}", product_ids)

                    # Create task for each wardrobe item
                    wardrobe_task = asyncio.create_task(wrapped_wardrobe_task(item, i))
                    task_map[wardrobe_task] = f"wardrobe_{i}"

                # PROCESS PSYCHOLOGIST & WARDROBE RETRIEVAL TASKS
                for completed_coroutine in asyncio.as_completed(task_map.keys()):
                    task_type, completed_task_result = await completed_coroutine

                    # Send message based on task type
                    if task_type == "psychologist":
                        await manager.send_personal_message(
                            json.dumps(
                                {"psychologist_response": completed_task_result}
                            ),
                            websocket,
                        )
                    elif task_type.startswith("wardrobe_"):
                        await manager.send_personal_message(
                            json.dumps({"wardrobe_retrieval": completed_task_result}),
                            websocket,
                        )
                logger.info("Finished processing secondary agents")
            else:
                logger.info("Not proceeding with secondary agents")

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}", exc_info=True)
    # finally:
    #     # Disconnect only if WebSocket is not already closed
    #     if not websocket.application_state == WebSocketState.DISCONNECTED:
    #         await manager.disconnect(client_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
