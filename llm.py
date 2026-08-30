import os
from openai import OpenAI

# DashScope provides an OpenAI-compatible endpoint
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Load system prompt from txt file
PROMPT_FILE = os.path.join(os.path.dirname(__file__), "system_instruction.txt")
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    system_instruction = f.read()

def summarizeLLMtool(prompt: str, image_url: str = None) -> str:
    """
    Summarizes chat messages or processes multimodal input using Qwen on OpenRouter.
    
    :param prompt: The formatted text messages/chat transcript to summarize.
    :param image_url: (Optional) The formatted list of captions w/ image attachments.
    :param model: The model name to use ("qwen-max" for text, "qwen-vl-max" for images).
    :return: Generated summary string.
    """
    
    # Text-only summary:
    model = "qwen/qwen-2.5-72b-instruct:free"

    # Image + Text multimodal summary:
    if image_url:
        model = "qwen/qwen2.5-vl-72b-instruct:free"

    if image_url:
        content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    else:
        content = prompt

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": content}
        ]
    )
    
    return response.choices[0].message.content

'''
1. Get SQL database
2. Create a function in db.py that filters the entire database's items with specific parameters and writes them all into 'prompt' variable.
3. Do the same with the items w/ images and make an 'image_url' variable
4. Use the 'prompt' and 'image_url' variables for the function.
'''