
from Utils import delete_punctuation
import json
import csv
import os


word_ids = {}


def create_new_id():
    return word_ids[max(word_ids, key=word_ids.get)] + 1 if len(word_ids) > 0 else 0


def bsbi(file_names: list, where_to_write_result: str = 'results/result_bsbi'):
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
                    if word not in word_ids:
                        word_ids[word] = create_new_id()
                    word_id = word_ids[word]
                    word_doc_id_list.append((word_id, file_indices[file]))

                if len(word_doc_id_list) == threshold:
                    word_doc_id_list.sort()
                    save_block_in_file(word_doc_id_list, where_to_write_result, block_number)
                    block_number += 1
                    word_doc_id_list = []

    word_doc_id_list.sort()
    save_block_in_file(word_doc_id_list, where_to_write_result, block_number)
    print('total number of words = ' + str(total_number))
    print('number of unique words = ' + str(len(word_ids)))
    with open('results/word_ids.txt', 'w') as file:
        file.write(json.dumps(word_ids))

    merge_blocks([where_to_write_result + str(number) + '.csv' for number in range(block_number + 1)])


def save_block_in_file(list_to_write: list, where_to_write_result: str, block_number: int):

    with open(where_to_write_result + str(block_number) + '.csv', "w") as file:
        writer = csv.writer(file)
        for item in list_to_write:
            writer.writerow(item)

    print(f'(word, document) pair block {block_number} size in kb = '
          + str(os.path.getsize(where_to_write_result) / 1000))


def merge_blocks(blocks: list, where_to_write_result: str = 'results/result_merged_bsbi'):
    inverted_index = {}

    for block in blocks:
        print(block)
        word_doc_id_list = []
        with open(block, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    word_doc_id_list.append(row)

            for item in word_doc_id_list:
                word = item[0]
                doc_id = item[1]
                if word not in inverted_index:
                    inverted_index[word] = {}

                if doc_id not in inverted_index[word]:
                    inverted_index[word][doc_id] = 0

                inverted_index[word][doc_id] += 1

    with open(where_to_write_result + '.txt', 'w') as file_for_result:
        file_for_result.write(json.dumps(inverted_index))

    print('merged bsbi size in kb = '
          + str(os.path.getsize(where_to_write_result) / 1000))


# результат на колекції
# (word, document) pair block size in kb = 12466.003
# total number of words = 1393312
# number of unique words = 34709
# розмір злитого інвертованого індекса
# merged bsbi size in kb = 967.455
# time = 75.32112693786621


# результат на колекції
# total number of words = 27743838
# number of unique words = 49452
# розмір злитого інвертованого індекса
# merged bsbi size in kb = 1302.394


# час злиття 20 файлів
# merged bsbi size in kb = 3207.055 (20 files)
# 637 seconds - time of merging of 20 files


# статистика на малій колекції
# 2597.676 - (word, document) pair block size
# 501.869 - merged bsbi size
# 454.736 - merged bsbi size with word ids
