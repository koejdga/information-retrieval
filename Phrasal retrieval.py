import json
import re
from Utils import delete_punctuation
from BooleanRetrieval import boolean_retrieval_indices
from Variables import file_collection


with open('results/result_coordinate.txt', 'r') as f:
    coordinate_index = json.loads(f.read())


def phrasal_retrieval(query: str):
    return retrieval_with_distance(re.sub('([ ])', r' /1 ', query))


def retrieval_with_distance(query: str):
    return [file_collection[i] for i in retrieval_with_distance_indices(query)]


def retrieval_with_distance_indices(query: str):
    query = query.split()
    query = [delete_punctuation(word) if word[0] != '/' else word for word in query]

    if check_query(query) is not None:
        return check_query(query)

    bool_query = ' '.join(word if word[0] != '/' else 'AND' for word in query)
    files = boolean_retrieval_indices(bool_query)

    first, second, distance = '', '', 0

    counter = 0
    for i in range(len(query)):
        counter += 1
        if query[i][0] == '/':
            distance = int(query[i][1:])
        elif first == '':
            first = query[i]
        elif second == '':
            second = query[i]

        if first != '' and second != '':
            files = two_words_retrieval(first, second, distance, files)
            first, second, distance = '', '', 0

    return files


def two_words_retrieval(first_word: str, second_word: str, distance: int, files: list):
    result = []
    for file_number in files:
        breaker = False
        for index in coordinate_index[first_word][str(file_number)]:
            counter = 1
            while counter <= distance:
                if index + counter in coordinate_index[second_word][str(file_number)]:
                    result.append(file_number)
                    breaker = True
                    break
                counter += 1
            if breaker:
                break

    return result


def check_query(query):
    if len(query) == 0:
        return 'Запит пустий'

    for i in range(len(query)):
        if i % 2 == 1:
            if query[i][0] == '/' and query[i][1:].isnumeric():
                pass
            else:
                return 'Неправильно сформульований запит'
    return None
