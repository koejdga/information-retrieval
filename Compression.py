
from VariableByteCoding import vb_encode, vb_decode
from Utils import delete_punctuation
import os
import csv
from Variables import file_collection

# region Creating index


def vb_create_inverted_index(file_names: list, where_to_write_index: str = 'results/vbc_inverted_index',
                             where_to_write_dict='dictionary.txt', where_to_write_block: str = 'results/bsbi_block'):
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

    for file in file_names:
        print(file)
        with open(file, "r") as txt_file:
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

                    write_block_in_file(word_doc_id_list, where_to_write_block + str(block_number) + '.csv')
                    block_number += 1
                    word_doc_id_list = []

    word_doc_id_list = sorted(word_doc_id_list, key=lambda tup: tup[0])
    write_block_in_file(word_doc_id_list, where_to_write_block + str(block_number) + '.csv')

    process_blocks(where_to_write_block, where_to_write_index, where_to_write_dict)
    print('total number of words = ' + str(total_number))
    print('end of vb_bsbi')


def write_block_in_file(list_to_write: list, where_to_write_result: str):

    with open(where_to_write_result, "w") as file:
        writer = csv.writer(file)
        for item in list_to_write:
            writer.writerow(item)

    print('(word, document) pair block size in kb = '
          + str(os.path.getsize(where_to_write_result) / 1000))


def process_blocks(block_template, where_to_write_index, where_to_write_dict):
    not_encoded_inverted_index = merge_blocks(block_template)  # формат {'слово': {файл: частота, файл: частота}}
    index_with_gaps = change_doc_ids_to_gaps(not_encoded_inverted_index) # формат {'слово': [файл, пробіл]}
    encoded_index = encode_dict_with_lists(index_with_gaps)
    save_dictionary_to_file(encoded_index, not_encoded_inverted_index, where_to_write_dict)
    save_inverted_index_to_file(encoded_index, where_to_write_index)


def merge_blocks(block_template: str = 'results/bsbi_block'):
    inverted_index = {}
    block_number = 0

    while os.path.isfile(block_template + str(block_number) + '.csv'):
        with open(block_template + str(block_number) + '.csv', 'r') as file:
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

    # тут по ідеї мають видалятися блоки os.remove("demofile.txt")
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
        encoded_dict_with_lists[key.encode("utf-8")] = vb_encode(dict_with_lists[key])
    return encoded_dict_with_lists


def save_dictionary_to_file(encoded_dict, not_encoded_dict, where_to_write_dict='dictionary.txt'):
    words_list = list(not_encoded_dict.keys())
    words_frequencies = [sum(files.values()) for files in not_encoded_dict.values()]
    file_pointers_list = []
    len_of_previous_list = 0
    for key in encoded_dict:
        if not file_pointers_list:
            file_pointers_list.append(0)
        else:
            file_pointers_list.append(file_pointers_list[-1] + len_of_previous_list)
        len_of_previous_list = len(encoded_dict[key])

    with open(where_to_write_dict, 'w') as f:
        for (word, word_frequency, file_pointer) in zip(words_list, words_frequencies, file_pointers_list):
            f.write("{0} {1} {2}\n".format(word, word_frequency, file_pointer))


def save_inverted_index_to_file(dict_with_lists, where_to_write_result):
    with open(where_to_write_result + '.bin', 'wb') as result_file:
        for key in dict_with_lists:
            for doc_id in dict_with_lists[key]:
                result_file.write(bytes([doc_id]))

# endregion

# region Getting inverted list from file


where_to_get_dict_from = 'dictionary.txt'
where_to_get_index_from = 'results/vbc_inverted_index.bin'
is_initialised = False
words = []
word_frequencies = []
file_pointers = []


def get_inverted_list(target_word: str):
    initialise()

    target_word_index = binary_search(words, target_word) if target_word in words else None
    if target_word_index is None:
        return "We haven't met your word"

    file_pointer = file_pointers[target_word_index]
    len_of_inverted_index = file_pointers[target_word_index+1] - file_pointers[target_word_index]

    with open(where_to_get_index_from, 'rb') as f:
        f.seek(file_pointer)
        encoded_inverted_list = f.read(len_of_inverted_index)
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
    if not is_initialised:
        global words, word_frequencies, file_pointers
        words, word_frequencies, file_pointers = get_dictionary_from_file()


def get_dictionary_from_file():
    words = []
    word_frequencies = []
    file_pointers = []

    with open(where_to_get_dict_from, 'r') as f:
        line = f.readline().split()
        while line:
            words.append(line[0])
            word_frequencies.append(int(line[1]))
            file_pointers.append(int(line[2]))
            line = f.readline().split()

    return words, word_frequencies, file_pointers


def change_gaps_to_doc_ids(list_with_gaps):
    for i in range(len(list_with_gaps)):
        if i != 0:
            list_with_gaps[i] += list_with_gaps[i - 1]

# endregion


vb_create_inverted_index(file_collection)
