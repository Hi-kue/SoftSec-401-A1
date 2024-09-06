from config.log_config import logging as log


lower_list = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
    "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
    "y", "z"
]

upper_list = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
    "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
    "W", "X", "Y", "Z"
]


def encrypt_content(text: str, shift: int) -> str:
    text_list = []
    position = 0

    text_list.append([ch for ch in text])

    for i in text_list:
        if i.isalpha():
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
    text_list = []
    position = 0

    text_list.append([ch for ch in text])

    for i in text_list:
        if i.isalpha():
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
