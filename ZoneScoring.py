from bs4 import BeautifulSoup
from Utils import delete_punctuation, final_processing
import json
from Variables import collection

# 1 - body
# 2 - title

with open('results/result_zone_scoring.txt', 'r') as f:
    zone_scoring_index = json.loads(f.read())
k = 10


def create_a_zone_scoring_index(file_names: list, where_to_write_result: str = 'results/result_zone_scoring.txt'):
    file_names = sorted(set(file_names))  # позбавляємося повторів файлів, якщо вони є
    zone_scoring_index_list = {}

    file_indices = {}
    index = 0
    for file in file_names:
        file_indices[file] = index
        index += 1

    for file in file_names:
        print(file)
        with open(file, "r", encoding="utf8") as f:
            soup = BeautifulSoup(f, 'html.parser')
            body = soup.find('body').get_text()
            title = soup.find('title').get_text().strip()
        body = body.split()
        title = title.split()
        for word in body:
            add_word(word, file_indices[file], 1, zone_scoring_index_list)
        for word in title:
            add_word(word, file_indices[file], 2, zone_scoring_index_list)

    final_processing(zone_scoring_index_list, where_to_write_result, 'zone scoring index')


def add_word(word: str, file_index: int, zone_index: int, zone_scoring_index_list: dict):
    word = delete_punctuation(word)

    zone_scoring_index_list[word] = [] if word not in zone_scoring_index_list else zone_scoring_index_list[word]

    new_value = str(file_index) + " " + str(zone_index)
    if new_value not in zone_scoring_index_list[word]:
        zone_scoring_index_list[word].append(new_value)


def zone_scoring_retrieval(query: str):
    query = query.split()
    query = [delete_punctuation(word) for word in query]

    file_relevance = {}
    result = []

    for word in query:
        inverted_index = zone_scoring_index[word]  # ["0 1", "1 1"]
        for item in inverted_index:
            file = int(item.split()[0])
            zone = int(item.split()[1])
            file_relevance[file] = 0 if file not in file_relevance else file_relevance[file]
            file_relevance[file] += get_g(zone) * 1

    max_value = max(file_relevance.values())  # maximum value
    counter = 0
    for key, value in file_relevance.items():
        counter += 1
        if counter <= k and value == max_value:
            result.append(key)

    return [collection[i] for i in result]


def get_g(zone: int):
    return zone



