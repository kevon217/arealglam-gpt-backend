# app/utils/load_assistants.py
from app.utils.oai_client_async import get_openai_client


async def get_assistant(assistant_id):
    client = get_openai_client()
    assistant = await client.beta.assistants.retrieve(assistant_id)
    return assistant


# async def load_assistants():
#     client = get_openai_client()

#     orchestrator_id = os.getenv("ORCHESTRATOR_ASSISTANT_ID")
#     psychologist_id = os.getenv("PSYCHOLOGIST_ASSISTANT_ID")
#     wardrobe_id = os.getenv("WARDROBE_ASSISTANT_ID")

#     orchestrator_assistant = await client.beta.assistants.retrieve(orchestrator_id)
#     psychologist_assistant = await client.beta.assistants.retrieve(psychologist_id)
#     wardrobe_assistant = await client.beta.assistants.retrieve(wardrobe_id)

#     return orchestrator_assistant, psychologist_assistant, wardrobe_assistant
