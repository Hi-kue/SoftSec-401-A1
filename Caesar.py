list = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
    "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
    "y", "z"
]


def shift(text, displacement):
    for i in text:
        shift_amount = (list.index(i) + displacement) % len(list)
        text = text.replace(i, list[shift_amount])
    return text


def unshift(text, displacement):
    for i in text:
        shift_amount = (list.index(i) - displacement) % len(list)
        text = text.replace(i, list[shift_amount])
    return text


num = 31
print(shift("wxyz", num))
print(unshift(shift("wxyz", num), num))
