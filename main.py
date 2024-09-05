from flask import Flask, request, jsonify
from config.log_config import logger as log
from config.response import HTTPResponses, HTTPResponse, set_custom_response
from dotenv import load_dotenv

import os

app = Flask(__name__)

load_dotenv(dotenv_path=".env")


@app.route("/api/v1/", methods=["GET"])
def index():
    return jsonify(HTTPResponses.OK.to_dict())


# TODO: Complete Implementation of this Route
@app.route("/api/v1/encrypt", methods=["POST"])
def encrypt_content():
    content = request.args.get("content")
    shift = int(request.args.get("shift"))

    if not content and not shift:
        return jsonify(HTTPResponses.BAD_REQUEST.to_dict())

    # TODO: Encryption Logic Here

    response = set_custom_response(
        200,
        "Encryption Successful",
        data={
            "content": encrypted_content,  # FIXME
        },
        error=None
    )

    return jsonify(response.to_dict())


# TODO: Complete Implementation of this Route
@app.route("/api/v1/decrypt", methods=["POST"])
def decrypt_content():
    content = request.args.get("content")
    shift = int(request.args.get("shift"))

    if not content and not shift:
        return jsonify(HTTPResponses.BAD_REQUEST.to_dict())

    response = set_custom_response(
        200,
        "Decryption Successful",
        data={
            "content": decrypted_content,  # FIXME
            "shift": shift
        },
        error=None
    )


# TODO: Complete Implementation of this Route
@app.route("/api/v1/hack_encrypt", methods=["POST"])
def hack_caesar_cipher():
    ciphertext = request.args.get("ciphertext")
    expected_content = request.args.get("expected_content")

    if not ciphertext and not expected_content:
        return jsonify(HTTPResponses.BAD_REQUEST.to_dict())

    response = set_custom_response(
        200,
        "Decryption Successful",
        data={
            "cipher_text": decrypted_content,
            "valid_shift": shift
            "expected_content": expected_content
        },
        error=None
    )