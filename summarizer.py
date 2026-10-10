'''
summarizer.py - Python library where all summarizing tasks are processed through
the Qwen LLM API

Instead of the Telegram bot typing its messages, it only has to run the functions here
and have completed AI summary responses ready for submission. The following commands in this
library has to handle the processing of all message buffer content and prepare AI-generated responses.

'''

import os, time
from openai import OpenAI, APIError

# DashScope provides an OpenAI-compatible endpoint
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://github.com/EAZYCODER2415/tg-niche-summarizer_bot",  # Required by OpenRouter
        "X-Title": "SMU Niche Summarizer Bot" # Required by OpenRouter
    }
)

# Load system prompt from txt file
PROMPT_FILE = os.path.join(os.path.dirname(__file__), "system_instruction.txt")
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    system_instruction = f.read()

# The FREE MODEL list (in case Qwen doesn't work)
# free_models = [
#     "meta-llama/llama-3.3-70b-instruct:free",
#     "google/gemini-2.0-flash-exp:free",    # Multimodal (Text + Vision)
#     "qwen/qwen2.5-vl-72b-instruct:free"    # Multimodal (Text + Vision - correct slug)
# ]

free_models = [
    "openrouter/free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "google/gemma-4-31b-it:free"
]

def summarizeLLMtool(prompt: str, file_url: str = None, link: str = None) -> str:
    """
    Summarizes chat messages or processes multimodal input using Qwen on OpenRouter.
    
    :param prompt: The formatted text messages/chat transcript to summarize.
    :param image_url: (Optional) The formatted list of captions w/ image attachments.
    :param model: The model name to use ("qwen-max" for text, "qwen-vl-max" for images).
    :return: Generated summary string.
    """

    # Base text model (for first try)
    model = "qwen/qwen-2.5-72b-instruct"

    # Separate URLs from raw document filenames
    urls = []
    doc_names = []

    if file_url:
        # Split by whitespace/newlines if file_url contains multiple bundled items
        items = file_url.split()
        for item in items:
            if item.startswith("http://") or item.startswith("https://"):
                urls.append(item)
            else:
                doc_names.append(item)

    # Base text message with any hidden document filenames included as context
    combined_text = f"Message: {prompt}"
    if doc_names:
        combined_text += f"\nAttachments: {', '.join(doc_names)}"

    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Build content list dynamically
            content = [
                {"type": "text", "text": combined_text}
            ]

            # Append image URLs cleanly
            if urls:
                model = "qwen/qwen-2.5-vl-72b-instruct:free"  # Switch to vision model
                for url in urls:
                    content.append({"type": "image_url", "image_url": {"url": urls}})

            response = client.chat.completions.create(
                model=model,
                extra_body={"models": free_models},
                messages=[
                    {
                        "role": "system",
                        "content": system_instruction,
                    },
                    {"role": "user", "content": content}
                ],
                timeout=25.0
            )

            return response.choices[0].message.content

        except APIError as e:
            print(f"[Attempt {attempt + 1}/{max_retries}] OpenRouter Error: {e}")
            if attempt == max_retries - 1:
                return f"⚠️ OpenRouter Error: Request failed after {max_retries} attempts."
            
            time.sleep(2 ** attempt + 1)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return f"⚠️ Summary unavailable: {str(e)}"

def checkForTopic(message: str, topic: str, file_url: str = None) -> bool:
    """
    Checks message for a specific topic input. Will return a boolean.
    """

    # Base text model (for first try)
    model = "qwen/qwen-2.5-72b-instruct"

    # Separate URLs from raw document filenames
    urls = []
    doc_names = []

    if file_url:
        # Split by whitespace/newlines if file_url contains multiple bundled items
        items = file_url.split()
        for item in items:
            if item.startswith("http://") or item.startswith("https://"):
                urls.append(item)
            else:
                doc_names.append(item)

    # Base text message with any hidden document filenames included as context
    combined_text = f"Message: {message}"
    if doc_names:
        combined_text += f"\nAttachments: {', '.join(doc_names)}"

    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Build content list dynamically
            content = [
                {"type": "topic", "topic": topic},
                {"type": "text", "text": combined_text}
            ]

            # Append image URLs cleanly
            if urls:
                model = "qwen/qwen-2.5-vl-72b-instruct:free"  # Switch to vision model
                for url in urls:
                    content.append({"type": "image_url", "image_url": {"url": urls}})

            response = client.chat.completions.create(
                model=model,
                extra_body={"models": free_models},
                messages=[
                    {
                        "role": "system",
                        "content": f"You are detecting whether the given message (or attached files) is related to the topic: {topic}. Output ONLY 'True' or 'False'."
                    },
                    {"role": "user", "content": content}
                ],
                timeout=25.0
            )

            return response.choices[0].message.content.strip() == "True"

        except APIError as e:
            print(f"[Attempt {attempt + 1}/{max_retries}] OpenRouter Error: {e}")
            if attempt == max_retries - 1:
                return f"⚠️ OpenRouter Error: Request failed after {max_retries} attempts."
            
            time.sleep(2 ** attempt + 1)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return f"⚠️ Summary unavailable: {str(e)}"

'''
1. Get SQL database
2. Create a function in db.py that filters the entire database's items with specific parameters and writes them all into 'prompt' variable.
3. Do the same with the items w/ images and make an 'image_url' variable
4. Use the 'prompt' and 'image_url' variables for the function.
'''