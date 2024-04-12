import xml.etree.ElementTree as ET
from Utils import delete_punctuation, final_processing
import json
from Variables import fb2_collection

# 1 - body
# 2 - title
# 3 - author

# with open('results/result_zone_scoring_fb2.txt', 'r') as f:
#     zone_scoring_index_fb2 = json.loads(f.read())
k = 10
zone_scoring_index_fb2 = 0


def create_a_zone_scoring_index(file_names: list, where_to_write_result: str = 'results/result_zone_scoring_fb2.txt'):
    print(len(file_names))
    file_names = sorted(set(file_names))  # позбавляємося повторів файлів, якщо вони є
    print(len(file_names))
    zone_scoring_index_list = {}

    file_indices = {}
    index = 0
    for file in file_names:
        file_indices[file] = index
        index += 1

    for file in file_names:
        print(file)
        tree = ET.parse(file)
        root = tree.getroot()

        title = root[0][0][2].text
        author = root[0][0][1].text

        body = ''
        for child2 in root[1]:
            for child3 in child2:
                if child3.text is not None:
                    body += child3.text

        if body:
            body = body.split()
            for word in body:
                add_word(word, file_indices[file], 1, zone_scoring_index_list)
        if title:
            title = title.split()
            for word in title:
                add_word(word, file_indices[file], 2, zone_scoring_index_list)
        if author:
            author = author.split()
            for word in author:
                add_word(word, file_indices[file], 3, zone_scoring_index_list)

    final_processing(zone_scoring_index_list, where_to_write_result, 'zone scoring index (fb2)')


def add_word(word: str, file_index: int, zone_index: int, zone_scoring_index_list: dict):
    word = delete_punctuation(word)

    zone_scoring_index_list[word] = [] if word not in zone_scoring_index_list else zone_scoring_index_list[word]

    new_value = str(file_index) + " " + str(zone_index)
    if new_value not in zone_scoring_index_list[word]:
        zone_scoring_index_list[word].append(new_value)


def zone_scoring_retrieval(query: str, inverted_index: str):
    with open(inverted_index, 'r') as f:
        global zone_scoring_index_fb2
        zone_scoring_index_fb2 = json.loads(f.read())

    query = query.split()
    query = [delete_punctuation(word) for word in query]

    file_relevance = {}

    for word in query:
        inverted_index = zone_scoring_index_fb2[word] if word in zone_scoring_index_fb2 else None  # ["0 1", "1 1"]
        if not inverted_index:
            continue
        for item in inverted_index:
            file = int(item.split()[0])
            zone = int(item.split()[1])
            file_relevance[file] = 0 if file not in file_relevance else file_relevance[file]
            file_relevance[file] += get_g(zone) * 1

    if file_relevance == {}:
        return []

    file_relevance = dict(sorted(file_relevance.items(), key=lambda value: value[1]))
    return list(file_relevance.keys())[0:k]


def get_g(zone: int):
    if zone == 1:
        return 1
    if zone == 2 or zone == 3:
        return 2

# create_a_zone_scoring_index(fb2_collection)
# print(zone_scoring_retrieval('a car'))
