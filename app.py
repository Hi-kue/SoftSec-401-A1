from flask import Flask, request, jsonify
import time
import logging as log
from rich.logging import RichHandler
import os
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from typing import Any, Dict, Optional


# HTTPResponse Configuration Code

class HTTPResponse:
    def __init__(self, status_code: int, message: str, data: Any = None, error: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        self.message = message
        self.data = data
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status_code": self.status_code,
            "message": self.message,
            "data": self.data,
            "error": self.error
        }


def set_custom_response(status_code: int, message: str, data: Any = None, error: Optional[Dict[str, Any]] = None):
    return HTTPResponse(status_code, message, data, error)


# Logging Configuration Code:

start_time = time.time()  # time::now
log.basicConfig(
    format="{asctime} - {levelname}: {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=log.INFO,
    handlers=[RichHandler()]
)
logger = log.getLogger("rich")

load_dotenv(dotenv_path=".env")

# AI Configuration Code

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


# Caesar Cipher Code:

lower_list = list("abcdefghijklmnopqrstuvwxyz")
upper_list = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def encrypt_content(text: str, shift: int) -> str:
    text_list = list(text)
    position = 0

    for i in text_list:
        if isinstance(i, str) and i.isalpha():
            if i.isupper():
                shift_amount = (upper_list.index(
                    i) + shift) % len(upper_list)
                text_list[position] = upper_list[shift_amount]
            else:
                shift_amount = (lower_list.index(
                    i) + shift) % len(lower_list)
                text_list[position] = lower_list[shift_amount]
        position += 1

    log.info(f"encryption successful! encrypted content: {text_list}")
    return "".join(text_list)


def decrypt_content(text: str, shift: int) -> str:
    text_list = list(text)
    position = 0

    for i in text_list:
        if isinstance(i, str) and i.isalpha():
            if i.isupper():
                shift_amount = (upper_list.index(i) - shift) % len(upper_list)
                text_list[position] = upper_list[shift_amount]
            else:
                shift_amount = (lower_list.index(i) - shift) % len(lower_list)
                text_list[position] = lower_list[shift_amount]
        position += 1

    log.info(f"decryption running... decrypted content: {text_list}")
    return "".join(text_list)


def hack_ceaser_cipher(text: str, expected: str) -> tuple:
    tries = 0

    if text == expected:
        return 0, text

    for i in range(1, 26):
        potential_decrypted_text = decrypt_content(text, i)

        log.info(f"trying shift: {i}, decrypted content: {potential_decrypted_text}")

        if potential_decrypted_text == expected:
            return i, decrypt_content(text, i)

        else:
            tries += 1
    return 0, "Failed to decrypt"


# Backend Flask Routing Code

app = Flask(__name__)

load_dotenv(dotenv_path=".env")


@app.route("/", methods=["GET"])
def home():
    return jsonify(HTTPResponse(
        200,
        "Welcome to Ceaser Cipher API",
        data=None,
        error=None
    ).to_dict())


@app.route("/api/v1", methods=["GET"])
def index():
    return jsonify(HTTPResponse(
        200,
        "Welcome to Ceaser Cipher API",
        data=None,
        error=None
    ).to_dict())


@app.route("/api/v1/encrypt", methods=["POST"])
def encrypt():
    content = ""
    shift = 0
    try:
        content = str(request.args.get("content"))
        shift = int(request.args.get("shift"))
    except:
        return jsonify(HTTPResponse(
            400,
            "Bad Request",
            data={"content": request.args.get("content"), "shift": request.args.get("shift")},
            error={"message": "ENCRYPTION FAILED due to invalid arguments. Try again."}
        ).to_dict())

    if not content or shift is None:
        return jsonify(HTTPResponse(
            400,
            "Bad Request",
            data=None,
            error={"message": "DECRYPTION FAILED due to missing arguments. Try again."}
        ).to_dict())

    encrypted_content = encrypt_content(str(content), int(shift))

    response = set_custom_response(
        200,
        "Encryption Successful",
        data={
            "content": encrypted_content,
        },
        error=None
    )

    return jsonify(response.to_dict())


@app.route("/api/v1/decrypt", methods=["POST"])
def decrypt():
    content = ""
    shift = 0
    try:
        content = str(request.args.get("content"))
        shift = int(request.args.get("shift"))
    except:
        return jsonify(HTTPResponse(
            400,
            "Bad Request",
            data={"content": request.args.get("content"), "shift": request.args.get("shift")},
            error={"message": "Invalid arguments. Try again."}
        ).to_dict())

    if not content or shift is None:
        return jsonify(HTTPResponse(
            400,
            "Bad Request",
            data=None,
            error={"message": "DECRYPTION FAILED due to missing arguments. Try again."}
        ).to_dict())

    decrypted_content = decrypt_content(str(content), int(shift))

    response = set_custom_response(
        200,
        "Decryption Successful",
        data={
            "content": decrypted_content,  # FIXME
            "shift": shift
        },
        error=None
    )

    return jsonify(response.to_dict())


@app.route("/api/v1/hack_encrypt", methods=["POST"])
def hack_encryption():
    ciphertext = request.args.get("ciphertext")
    expected_content = request.args.get("expected_content")

    if not ciphertext or not expected_content:
        return jsonify(HTTPResponse(
            400,
            "Bad Request",
            data=None,
            error={"message": "DECRYPTION FAILED due to missing arguments. Try again."}
        ).to_dict())

    shift, decrypted_content = hack_ceaser_cipher(text=ciphertext, expected=expected_content)

    if decrypted_content == expected_content:
        response = set_custom_response(
            200,
            "Hack Successful",
            data={
                "content": decrypted_content,
                "valid_shift": shift,
                "expected_content": expected_content
            },
            error=None
        )
    else:
        response = set_custom_response(
            400,
            "Hack Failed!, Double-check the expected_content parameter.",
            error="HACK FAILED!"
        )

    return jsonify(response.to_dict())


@app.route("/api/v1/decrypt_ai", methods=["POST"])
def decrypt_with_ai():
    encrypted_content = request.args.get("encrypted_content")
    expected_content = request.args.get("expected_content")

    if not encrypted_content and not expected_content:
        return jsonify(HTTPResponse(
            400,
            "Bad Request",
            data=None,
            error={"message": "Bad Request was Made"}
        ).to_dict())

    prompt = (f"Decrypt the following content: {encrypted_content}, "
              "determine the shift and provide the decrypted content."
              f"The expected content is: {expected_content}.")

    ai_response = send_request(role="user", query=prompt)

    response = set_custom_response(
        200,
        "Decryption Successful",
        data={
            "content": ai_response,
            "expected_content": expected_content
        },
        error=None
    )

    return jsonify(response.to_dict())


if __name__ == "__main__":
    app.run(port=os.getenv("PORT"), debug=True)
