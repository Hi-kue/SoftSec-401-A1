from config.log_config import logging as log

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

    log.info(f"decryption successful! decrypted content: {text_list}")
    return "".join(text_list)


def hack_ceaser_cipher(text: str, expected: str) -> tuple:
    tries = 0

    for i in range(1, 26):
        potential_decrypted_text = decrypt_content(text, i)

        log.info(f"trying shift: {i}, decrypted content: {potential_decrypted_text}")

        if potential_decrypted_text == expected:
            return i, decrypt_content(text, i)

        else:
            tries += 1
