from VariableByteCoding import vb_encode, vb_decode
from Utils import delete_punctuation
import os
import csv
from Variables import big_collection
from enum import IntEnum
import time

# region Creating index


def vb_create_inverted_index(file_names: list, where_to_write_index: str = 'results/vbc_inverted_index_v2',
                             where_to_write_dict='dictionary2', where_to_write_block: str = 'results/bsbi_block_v2_'):
    file_names = sorted(set(file_names))  # позбавляємося повторів файлів, якщо вони є
    word_doc_id_list = []
    block_number = 0
    threshold = 10000000
    total_number = 0

    file_indices = {}
    index = 0
    for file in file_names:
        file_indices[file] = index
        index += 1

    counter = 0
    for file in file_names:
        counter += 1
        print(str(counter) + ' ' + file)
        with open(file, "r", encoding="utf8") as txt_file:
            file_content = txt_file.readlines()
        for item in file_content:
            array_of_words = item.lower().split()
            for word in array_of_words:
                total_number += 1
                word = delete_punctuation(word)
                if len(word) > 0:
                    word_doc_id_list.append((word, file_indices[file]))

                if len(word_doc_id_list) == threshold:
                    word_doc_id_list = sorted(word_doc_id_list, key=lambda tup: tup[0])

                    save_block_in_file(word_doc_id_list, where_to_write_block, block_number)
                    block_number += 1
                    word_doc_id_list = []

    word_doc_id_list = sorted(word_doc_id_list, key=lambda tup: tup[0])
    save_block_in_file(word_doc_id_list, where_to_write_block, block_number)

    process_blocks(where_to_write_block, where_to_write_index, where_to_write_dict)
    print('total number of words = ' + str(total_number))
    print('end of vb_bsbi')


def save_block_in_file(list_to_write: list, where_to_write_result: str, block_number: int):
    with open(where_to_write_result + str(block_number) + '.csv', "w") as file:
        writer = csv.writer(file)
        for item in list_to_write:
            writer.writerow(item)

    print('(word, document) pair block size in kb = '
          + str(os.path.getsize(where_to_write_result + str(block_number) + '.csv') / 1000))


def process_blocks(block_template, where_to_write_index, where_to_write_dict):
    print('merging')
    not_encoded_inverted_index = merge_blocks(block_template)  # формат {'слово': {файл: частота, файл: частота}}
    print('creating index with gaps')
    index_with_gaps = change_doc_ids_to_gaps(not_encoded_inverted_index)  # формат {'слово': [файл, пробіл]}
    print('creating encoded index')
    encoded_index = encode_dict_with_lists(index_with_gaps)
    print('saving dictionary')
    save_dictionary_to_file(encoded_index, not_encoded_inverted_index, where_to_write_dict)
    print('saving inverted index')
    save_inverted_index_to_file(encoded_index, where_to_write_index)


def merge_blocks(block_template: str = 'results/bsbi_block_v2_'):
    inverted_index = {}
    block_number = 0

    while os.path.isfile(block_template + str(block_number) + '.csv'):
        with open(block_template + str(block_number) + '.csv', 'r') as file:
            print('processing ' + str(block_number) + ' block')
            reader = csv.reader(file)
            for row in reader:
                if row:
                    word = row[0]
                    doc_id = int(row[1])
                    if word not in inverted_index:
                        inverted_index[word] = {}

                    if doc_id not in inverted_index[word]:
                        inverted_index[word][doc_id] = 0

                    inverted_index[word][doc_id] += 1
        os.remove(block_template + str(block_number) + '.csv')
        block_number += 1

    # формат {'слово': [файл: частота, файл: частота]}
    return inverted_index


def change_doc_ids_to_gaps(inverted_index):
    index_with_gaps = {}
    for word in inverted_index:
        current_real_index = 0
        index_with_gaps[word] = []
        for doc_id in inverted_index[word]:
            index_with_gaps[word].append(doc_id - current_real_index)
            current_real_index += index_with_gaps[word][-1]
    return index_with_gaps


def encode_dict_with_lists(dict_with_lists):
    encoded_dict_with_lists = {}
    for key in dict_with_lists:
        encoded_dict_with_lists[key] = vb_encode(dict_with_lists[key])
    return encoded_dict_with_lists


def save_dictionary_to_file(encoded_dict, not_encoded_dict, where_to_write_dict='dictionary2'):
    words_list = list(not_encoded_dict.keys())
    words_string = ''.join(str(e) for e in words_list)
    word_pointers_list = [0]
    for word in words_list:
        word_pointers_list.append(len(word))
    word_pointers_list.pop()

    words_frequencies = [sum(files.values()) for files in not_encoded_dict.values()]

    file_pointers_list = [0]
    for word in encoded_dict:
        file_pointers_list.append(len(encoded_dict[word]))
    file_pointers_list.pop()

    with open(where_to_write_dict + '.bin', 'wb') as f:
        f.write(words_string.encode(encoding='ascii'))
        f.write(b'\n')
        for (word_pointer, word_frequency, file_pointer) in zip(word_pointers_list, words_frequencies,
                                                                file_pointers_list):
            f.write(bytes(vb_encode([word_pointer, word_frequency, file_pointer])))


def save_inverted_index_to_file(dict_with_lists, where_to_write_result):
    with open(where_to_write_result + '.bin', 'wb') as result_file:
        for key in dict_with_lists:
            for doc_id in dict_with_lists[key]:
                result_file.write(bytes([doc_id]))


# endregion

# region Getting inverted list from file


where_to_get_dict_from = 'dictionary3.bin'
where_to_get_index_from = 'results/vbc_inverted_index_v3.bin'
is_initialised = False
word_string = ''
word_pointers = []
word_frequencies = []
file_pointers = []


def get_inverted_list(target_word: str):
    initialise()

    target_word_index = binary_search_v2(word_string, word_pointers, target_word)
    if target_word_index is None:
        return "We haven't met your word"

    # file_pointer = file_pointers[target_word_index]
    file_pointer = get_pointer(target_word_index, file_pointers)
    len_of_inverted_index = get_pointer(target_word_index + 1, file_pointers) \
                            - get_pointer(target_word_index, file_pointers) \
        if target_word_index != len(file_pointers) - 1 else None

    with open(where_to_get_index_from, 'rb') as f:
        f.seek(file_pointer)
        if len_of_inverted_index:
            encoded_inverted_list = f.read(len_of_inverted_index)
        else:
            encoded_inverted_list = f.read()
        result = []
        for number in encoded_inverted_list:
            result.append(number)
        result = vb_decode(result)
        change_gaps_to_doc_ids(result)
        return result


def binary_search(array, to_find):
    lo = 0
    hi = len(array) - 1

    while hi - lo > 1:
        mid = (hi + lo) // 2
        if array[mid] < to_find:
            lo = mid + 1
        else:
            hi = mid

    if array[lo] == to_find:
        return lo
    elif array[hi] == to_find:
        return hi
    else:
        return None


def initialise():
    print('initialising')
    start = time.time()
    global is_initialised
    if not is_initialised:
        global word_string, word_pointers, word_frequencies, file_pointers
        word_string, word_pointers, word_frequencies, file_pointers = get_dictionary_from_file()
    is_initialised = True
    end = time.time()
    print('initialisation lasted ' + str(end - start) + ' seconds')


def get_dictionary_from_file():
    word_string = ''
    word_pointers = []
    word_frequencies = []
    file_pointers = []

    class State(IntEnum):
        WORD_STR = 1
        WORD_PTR = 2
        INDEX_PTR = 3
    current = State.WORD_STR

    with open(where_to_get_dict_from, 'rb') as f:
        print('reading dictionary')
        byte = f.read(1)
        while byte != b'\n':
            word_string += byte.decode('ascii')
            byte = f.read(1)

        print('word string is ready')

        byte = f.read(1)
        while byte:
            byte = int.from_bytes(byte, 'little')
            if current == State.WORD_STR:
                word_pointers.append(byte)
            elif current == State.WORD_PTR:
                word_frequencies.append(byte)
            elif current == State.INDEX_PTR:
                file_pointers.append(byte)
            if byte >= 128:
                current = current + 1 if int(current) < len(State) else 1
            byte = f.read(1)

    word_pointers = vb_decode(word_pointers)
    word_frequencies = vb_decode(word_frequencies)
    file_pointers = vb_decode(file_pointers)

    return word_string, word_pointers, word_frequencies, file_pointers


def change_gaps_to_doc_ids(list_with_gaps):
    for i in range(len(list_with_gaps)):
        if i != 0:
            list_with_gaps[i] += list_with_gaps[i - 1]


def get_word_from_string(dict_string, pointer_to_word, len_of_word=None):
    if len_of_word:
        word = dict_string[pointer_to_word: pointer_to_word + len_of_word]
    else:
        word = dict_string[pointer_to_word:]
    return word


def get_pointer(index, list_with_gaps):
    return sum(list_with_gaps[:index + 1])


def binary_search_v2(dict_string, pointers_in_string, to_find):
    lo = 0
    hi = len(pointers_in_string) - 1

    while hi - lo > 1:
        mid = (hi + lo) // 2
        file_pointer = get_pointer(mid, pointers_in_string)
        len_of_word = pointers_in_string[mid + 1] if mid != len(pointers_in_string) - 1 else None
        if get_word_from_string(dict_string, file_pointer, len_of_word) < to_find:
            lo = mid + 1
        else:
            hi = mid

    file_pointer = get_pointer(lo, pointers_in_string)
    len_of_word = pointers_in_string[lo + 1] if lo != len(pointers_in_string) - 1 else None
    if get_word_from_string(dict_string, file_pointer, len_of_word) == to_find:
        return lo
    else:
        file_pointer = get_pointer(hi, pointers_in_string)
        len_of_word = pointers_in_string[hi + 1] if hi != len(pointers_in_string) - 1 else None
        if get_word_from_string(dict_string, file_pointer, len_of_word) == to_find:
            return hi
    return None


# endregion

# vb_create_inverted_index(file_collection)

# vb_create_inverted_index(filelist,
#                          'results/vbc_inverted_index_v3', 'dictionary3', 'results/bsbi_block_v3_')
# total number of words = 1183681325 - це на повній колекції
# 117 блоків

# total number of words = 304024189 - це на чверті колекції
# process_blocks('results/bsbi_block_v3_', 'results/vbc_inverted_index_v3', 'dictionary3')

print('end')
