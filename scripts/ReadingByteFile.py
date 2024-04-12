from VariableByteCoding import vb_decode


def get_inverted_list(target_word: str):
    with open('results/vbc_inverted_index0.bin', 'rb') as f:
        byte = f.read(1)
        current_word = ''
        while byte:
            if byte.isalpha():
                current_word += byte.decode("utf-8")
            else:
                if target_word == current_word:
                    result = []
                    while not byte.isalpha() and byte:
                        result.append(int.from_bytes(byte, byteorder='little'))
                        byte = f.read(1)
                    result = vb_decode(result)
                    change_gaps_to_doc_ids(result)
                    return result
                else:
                    current_word = ''
            byte = f.read(1)
    return "We haven't met your word"


def change_gaps_to_doc_ids(list_with_gaps):
    for i in range(len(list_with_gaps)):
        if i != 0:
            list_with_gaps[i] += list_with_gaps[i - 1]
