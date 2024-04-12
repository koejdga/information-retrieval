from Utils import delete_punctuation, final_processing
from Variables import file_collection


def create_an_inverted_two_word_index(file_names: list, where_to_write_result: str = 'results/result_two_words.txt'):
    file_names = sorted(set(file_names))  # позбавляємося повторів файлів, якщо вони є
    inverted_index_list = {}

    file_indices = {}
    index = 0
    for file in file_names:
        file_indices[file] = index
        index += 1

    for file in file_names:
        temp = ''
        with open(file, "r") as txt_file:
            file_content = txt_file.readlines()
        for item in file_content:
            array_of_words = item.lower().split()
            for word in array_of_words:

                word = delete_punctuation(word)
                if temp == '':
                    temp = word
                    continue

                result = f'{temp} {word}'
                inverted_index_list[result] = [] if result not in inverted_index_list else inverted_index_list[result]

                if file_indices[file] not in inverted_index_list[result]:
                    inverted_index_list[result].append(file_indices[file])

                temp = word

    final_processing(inverted_index_list, where_to_write_result, 'inverted two word index')


def create_a_coordinate_index(file_names: list, where_to_write_result: str = 'results/result_coordinate.txt'):
    file_names = sorted(set(file_names))  # позбавляємося повторів файлів, якщо вони є
    inverted_index_list = {}

    file_indices = {}
    index = 0
    for file in file_names:
        file_indices[file] = index
        index += 1

    for file in file_names:
        counter = 0

        with open(file, "r") as txt_file:
            file_content = txt_file.readlines()
        for item in file_content:
            array_of_words = item.lower().split()
            for word in array_of_words:
                counter += 1

                word = delete_punctuation(word)

                inverted_index_list[word] = {} if word not in inverted_index_list else inverted_index_list[word]

                inverted_index_list[word][file_indices[file]] = [] \
                    if file_indices[file] not in inverted_index_list[word] \
                    else inverted_index_list[word][file_indices[file]]

                inverted_index_list[word][file_indices[file]].append(counter)

    final_processing(inverted_index_list, where_to_write_result, 'coordinate index')
