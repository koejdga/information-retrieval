import json
import os
import string
from Variables import file_collection


def create_a_dictionary(file_names: list, where_to_write_result: str = 'results/result.txt'):
    dictionary = []
    file_names = sorted(set(file_names))  # позбавляємося повторів файлів, якщо вони є
    size_of_collection = 0
    size_in_kb = 0

    for file in file_names:
        size_in_kb += os.path.getsize(file) / 1000
        with open(file, "r") as txt_file:
            file_content = txt_file.readlines()
        for item in file_content:
            array_of_words = item.lower().split()
            size_of_collection += len(array_of_words)
            for word in array_of_words:

                while len(word) > 0 and word[0] in string.punctuation:
                    word = word[1:]
                while len(word) > 0 and word[-1] in string.punctuation:
                    word = word[:-1]

                if word not in dictionary:
                    dictionary.append(word)

    dictionary.remove('')

    with open(where_to_write_result, 'w') as file:
        file.write(json.dumps(dictionary))
    print('collection size = ' + str(size_of_collection))
    print('dictionary size = ' + str(len(dictionary)))
    print('collection size in kb = ' + str(size_in_kb))
    print('dictionary size in kb = ' + str(os.path.getsize(where_to_write_result) / 1000))


create_a_dictionary(file_collection)