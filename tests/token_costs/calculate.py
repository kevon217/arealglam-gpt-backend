import json
import tiktoken
from pathlib import Path
from datetime import datetime
from app.assistants.prompts import cfo, psychologist, wardrobe

# Initialize TikToken encoding
encoding = tiktoken.get_encoding("cl100k_base")

# Define your prompts with model and expected response token count
prompts = [
    {
        "name": "chief_fashion_adviser",
        "text": cfo.cfo_instructions,
        "model": "gpt-4-1106-preview",
        "response_tokens": 100,  # Example expected response token count
        "input_tokens": 50,  # Manually entered expected input tokens
    },
    {
        "name": "psychologist",
        "text": psychologist.psychologist_instructions,
        "model": "gpt-4-1106-preview",
        "response_tokens": 350,
        "input_tokens": 100,
    },
    {
        "name": "wardrobe_retriever",
        "text": wardrobe.wardrobe_instructions,
        "model": "gpt-4-1106-preview",
        "response_tokens": 350,
        "input_tokens": 100,
    },
]

# Token costs per 1K tokens
costs_per_1k_tokens = {"gpt-4-1106-preview": 0.01}  # $0.01 per 1K tokens

# Initialize the basis costs and total cost
basis_costs = {}
total_cost = 0

# Calculating costs for each prompt
for prompt in prompts:
    prompt_name = prompt["name"]
    model = prompt["model"]
    input_tokens = prompt["input_tokens"]
    custom_instructions_tokens = len(encoding.encode(prompt["text"]))
    response_tokens = prompt["response_tokens"]
    total_tokens = input_tokens + custom_instructions_tokens + response_tokens
    cost_per_1k = costs_per_1k_tokens[model]
    total_cost_for_prompt = (total_tokens / 1000) * cost_per_1k

    # Adding to basis_costs
    basis_costs[prompt_name] = {
        "model": model,
        "cost_per_1k_tokens": cost_per_1k,
        "expected_input_tokens": input_tokens,
        "custom_instructions_tokens": custom_instructions_tokens,
        "expected_output_tokens": response_tokens,
        "total_tokens": total_tokens,
        "total_cost": total_cost_for_prompt,
    }

    # Accumulate total cost
    total_cost += total_cost_for_prompt

# Creating the final JSON structure
final_output = {"basis_costs": basis_costs, "total_cost": total_cost}

# Printing the JSON output
print(json.dumps(final_output, indent=4))

# Save costs to JSON file
file_path = Path.cwd() / "tests" / "token_costs" / "token_costs.json"
file_path = file_path.with_name(
    f"{file_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_path.suffix}"
)
with open(file_path, "w") as f:
    json.dump(final_output, f, indent=4)
