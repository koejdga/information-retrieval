import json
from Variables import file_collection

# file_collection - список директорій файлів

with open('results/result_index.txt', 'r') as f:
    inverted_index = json.loads(f.read())


def check_query(query):
    if len(query) == 0:
        return 'Запит пустий'

    list_without_not = list(filter(lambda val: val != 'NOT', query))
    for i in range(len(list_without_not)):
        if i % 2 == 1 and list_without_not[i] not in ('AND', 'OR'):
            return 'Помилка в заданні запиту'

    return None


def boolean_retrieval_indices(query: str):
    query = query.split()

    if check_query(query) is not None:
        return check_query(query)

    if 'OR' not in query and 'NOT' not in query:
        query = filter(lambda val: val != 'AND', query)
        return quick_retrieval_with_and([inverted_index[word] for word in query])
    
    result = []
    temp = []

    intersect_list = False
    union_list = False
    not_list = False

    for word in query:
        if word not in ('AND', 'OR', 'NOT'):
            if not result:
                result = inverted_index[word]
            else:
                temp = inverted_index[word]

            if not_list:
                if not temp:
                    result = complement(result, len(file_collection))
                else:
                    temp = complement(temp, len(file_collection))
                not_list = False
            if intersect_list:
                result = intersection(result, temp)
                intersect_list = False
                temp = []
            elif union_list:
                result = union(result, temp)
                union_list = False
                temp = []
        elif word == 'AND':
            intersect_list = True
        elif word == 'OR':
            union_list = True
        elif word == 'NOT':
            not_list = True

    return result


def boolean_retrieval(query: str):
    return [file_collection[i] for i in boolean_retrieval_indices(query)]


def intersection(first: list, second: list):
    result = []
    i = j = 0
    while i < len(first) and j < len(second):
        if first[i] == second[j]:
            result.append(first[i])
            i += 1
            j += 1
        elif first[i] > second[j]:
            j += 1
        elif first[i] < second[j]:
            i += 1

    return result


def union(first: list, second: list):
    result = []
    i = j = 0
    while i < len(first) and j < len(second):
        if first[i] == second[j]:
            result.append(first[i])
            i += 1
            j += 1
        elif first[i] > second[j]:
            result.append(second[j])
            j += 1
        elif first[i] < second[j]:
            result.append(first[i])
            i += 1
    if i < len(first):
        result.append(first[i])
        i += 1
    elif j < len(second):
        result.append(second[j])
        j += 1
    return result


def complement(list_of_indices, collection_size):
    return [x for x in range(collection_size) if x not in list_of_indices]


def quick_retrieval_with_and(query):
    return list(set.intersection(*map(set, query)))
