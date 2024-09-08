from flask import Flask, request, jsonify
from ceaser import encrypt_content, decrypt_content, hack_ceaser_cipher
from config.response import HTTPResponse, set_custom_response
from config.ai_config import client, send_request
from dotenv import load_dotenv

import os

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
    content = request.args.get("content")
    shift = int(request.args.get("shift"))

    if not content and not shift:
        return jsonify(HTTPResponse(
            400,
            "Bad Request",
            data=None,
            error={"message": "Bad Request was Made"}
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
    content = request.args.get("content")
    shift = int(request.args.get("shift"))

    if not content and not shift:
        return jsonify(HTTPResponse(
            400,
            "Bad Request",
            data=None,
            error={"message": "Bad Request was Made"}
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

    if not ciphertext and not expected_content:
        return jsonify(HTTPResponse(
            400,
            "Bad Request",
            data=None,
            error={"message": "Bad Request was Made"}
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
