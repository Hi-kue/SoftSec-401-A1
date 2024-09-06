list = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
    "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
    "y", "z"
]


def shift(text, displacement):
    text_list = []
    position = 0
    for i in text:
        text_list.append(i)
    for i in text_list:
        shift_amount = (list.index(i) + displacement) % len(list)
        text_list[position] = list[shift_amount]
        position += 1
    return "".join(text_list)


def unshift(text, displacement):
    text_list = []
    position = 0
    for i in text:
        text_list.append(i)
    for i in text_list:
        shift_amount = (list.index(i) - displacement) % len(list)
        text_list[position] = list[shift_amount]
        position += 1
    return "".join(text_list)


num = 31
print(shift("johnjon", num))
print(unshift(shift("johnjon", num), num))
