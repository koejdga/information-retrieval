
from Utils import delete_punctuation, final_processing
from Variables import file_collection


def create_a_3_gram_index(file_names: list, where_to_write_result: str = 'results/result_3_gram_index.txt'):
    file_names = sorted(set(file_names))  # позбавляємося повторів файлів, якщо вони є
    three_gram_index_list = {}

    file_indices = {}
    index = 0
    for file in file_names:
        file_indices[file] = index
        index += 1

    for file in file_names:
        with open(file, "r") as txt_file:
            file_content = txt_file.readlines()
        for item in file_content:
            array_of_words = item.lower().split()
            for unit in array_of_words:

                words = delete_punctuation(unit)

                for word in words:
                    trigram = '$'
                    for i in range(len(word)-1):
                        trigram = create_trigram(word, i, trigram)

                        if trigram not in three_gram_index_list.keys():
                            three_gram_index_list[trigram] = []

                        if word not in three_gram_index_list[trigram]:
                            three_gram_index_list[trigram].append(word)

                        trigram = ''

    final_processing(three_gram_index_list, where_to_write_result, '3 gram index')


def create_trigram(word: str, i: int, trigram: str):
    trigram += word[i]
    trigram += word[i+1]
    if i+2 < len(word) and len(trigram) < 3:
        trigram += word[i+2]
    if len(trigram) < 3:
        trigram += '$'

    return trigram


