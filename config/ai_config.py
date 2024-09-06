import os

from openai import OpenAI, OpenAIError
from config.log_config import logger as log
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

PRIMARY_MODEL = "meta-llama/llama-3.1-8b-instruct:free"
SYSTEM_PROMPT = ("You are a deciphering AI model that specializes in the Caesar Cipher algorithm. "
                 "Your task is to decipher the encrypted message provided by the user. "
                 "You should determine the shift used in the Caesar Cipher and provide the decrypted message. "
                 "At the end of your response, clearly state the shift value and the deciphered message. "
                 "Do not provide any additional information or engage in other tasks, be short and concise. "
                 "Focus solely on decrypting the given message using the Caesar Cipher method.")


def send_request(role: str = "user", query: str = None) -> str:
    if query is None or query == "":
        raise ValueError("Query provided is empty.")

    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct:free",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": role, "content": query}
            ],
            # top_p=1,
            # temperature=1,
            # frequency_penalty=0,
            # presence_penalty=0,
        )

        log.info(f"Received (AI): {completion.choices[0].message.content}")
        return completion.choices[0].message.content

    except Exception as e:
        log.error(f"Error: {e}")
        raise OpenAIError(f"Error: {e}")
