import string
import json
import os


def delete_punctuation(word : str):
    word = word.lower()

    while len(word) > 0 and word[0] in string.punctuation:
        word = word[1:]
    while len(word) > 0 and word[-1] in string.punctuation:
        word = word[:-1]

    new_word = ''
    for char in word:
        if char.isascii():
            new_word += char
    if new_word != '':
        return new_word


def final_processing(index_list: dict, where_to_write_result: str, list_name: str):
    index_list = dict(sorted(index_list.items()))
    if '' in index_list:
        del index_list['']

    with open(where_to_write_result, 'w') as file:
        file.write(json.dumps(index_list))

    print(list_name + ' size in kb = ' + str(os.path.getsize(where_to_write_result) / 1000))
    return index_list
