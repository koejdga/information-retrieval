
def vb_encode_number(number):
    bytes_list = []
    while True:
        if len(bytes_list) > 0:
            bytes_list.insert(0, number % 128)
        else:
            bytes_list.append(number % 128)
        if number < 128:
            break
        number //= 128
    bytes_list[len(bytes_list) - 1] += 128
    return bytes_list


def vb_encode(numbers):
    result = []
    for number in numbers:
        bytes_list = vb_encode_number(number)
        result.extend(bytes_list)
    return result


def vb_decode(bytestream):
    numbers = []
    n = 0
    for i in range(len(bytestream)):
        if bytestream[i] < 128:
            n = 128 * n + bytestream[i]
        else:
            n = 128 * n + (bytestream[i] - 128)
            numbers.append(n)
            n = 0
    return numbers


print(vb_encode_number(825))
