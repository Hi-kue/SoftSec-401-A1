lower_list = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
    "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
    "y", "z"
]

upper_list = []

for i in lower_list:
    upper_list.append(i.upper())

print(upper_list)
print(lower_list)


def shift(text, displacement):
    text_list = []
    position = 0
    for i in text:
        text_list.append(i)
    for i in text_list:
        if i != " ":
            if i.isupper():
                shift_amount = (upper_list.index(
                    i) + displacement) % len(upper_list)
                text_list[position] = upper_list[shift_amount]
            else:
                shift_amount = (lower_list.index(
                    i) + displacement) % len(lower_list)
                text_list[position] = lower_list[shift_amount]
        position += 1
    return "".join(text_list)


def unshift(text, displacement):
    text_list = []
    position = 0
    for i in text:
        text_list.append(i)
    for i in text_list:
        if i != " ":
            if i.isupper():
                shift_amount = (upper_list.index(
                    i) - displacement) % len(upper_list)
                text_list[position] = upper_list[shift_amount]
            else:
                shift_amount = (lower_list.index(
                    i) - displacement) % len(lower_list)
                text_list[position] = lower_list[shift_amount]
        position += 1
    return "".join(text_list)


num = 1
text = "aBc DeF"
print(shift(text, num))
print(unshift(shift(text, num), num))
