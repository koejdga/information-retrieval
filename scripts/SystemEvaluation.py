from enum import Enum

from rank_bm25 import BM25Okapi

from Variables import cranfield_collection
from FB2 import FictionBook2
from ZoneScoringFB2 import create_a_zone_scoring_index, zone_scoring_retrieval

all_1400_articles = 'D:/NaUKMA/year 2/інфопошук/cranfield collection/cran.all.1400'
queries = 'D:/NaUKMA/year 2/інфопошук/cranfield collection/cran.qry'
relevance = 'D:/NaUKMA/year 2/інфопошук/cranfield collection/cranqrel'

relevance_list = {}
files_list = {}


def create_fb2_book(title: str, author: str, body: str, where_to_write_file: str):
    """
        Parameters
        ----------
        where_to_write_file : str
            The location of a new file without extension
        """
    book = FictionBook2()
    book.titleInfo.title = title
    book.titleInfo.authors = [author]
    book.chapters = [("", [body])]
    book.write(where_to_write_file + '.fb2')


def parse_files_to_fb2():
    with open(all_1400_articles, 'r') as f:
        file_content = f.readlines()
    current_state = 0
    counter = 2
    body, title, author = '', '', ''

    class Reading(Enum):
        BODY = 1
        TITLE = 2
        AUTHOR = 3
        SKIP = 4

    for item in file_content:
        if item == f'.I {counter}\n' and body != '':
            print('adding new fb2 file')
            create_fb2_book(title, author, body,
                            f"D:/NaUKMA/year 2/інфопошук/cranfield collection/cranfield unpacked/article_{counter - 1}")
            title = ''
            author = ''
            body = ''
            counter += 1

        if item in ('.T\n', '.A\n', '.B\n', '.W\n'):
            if item == '.T\n':
                current_state = Reading.TITLE
            elif item == '.A\n':
                current_state = Reading.AUTHOR
            elif item == '.B\n':
                current_state = Reading.SKIP
            elif item == '.W\n':
                current_state = Reading.BODY

        else:
            if current_state == Reading.TITLE:
                title += item
            elif current_state == Reading.AUTHOR:
                author += item
            elif current_state == Reading.BODY:
                body += item

    create_fb2_book(title, author, body,
                    f"D:/NaUKMA/year 2/інфопошук/cranfield collection/cranfield unpacked/article_{counter - 1}")


def parse_files_to_str():
    with open(all_1400_articles, 'r') as f:
        file_content = f.readlines()
    counter = 0

    for item in file_content:
        if f'.I' in item:
            counter += 1

        if item not in ('.T\n', '.A\n', '.B\n', '.W\n'):
            if counter not in files_list:
                files_list[counter] = ""
            files_list[counter] += item
            files_list[counter] += " "


def parse_queries():
    with open(queries, 'r') as f:
        file_content = f.readlines()

    file_content = file_content[1:]

    query = ''
    all_queries = []
    counter = 0

    for item in file_content:

        if '.I' in item and query != '':
            counter += 1
            all_queries.append(query)
            query = ''

        elif item != '.W\n':
            query += item.replace('\n', ' ')

    all_queries.append(query)
    return all_queries


def parse_relevance_results():
    with open(relevance, 'r') as f:
        file_content = f.readlines()

    for item in file_content:
        item = [int(num) for num in item.split()]
        if item[2] < 4:
            if item[0] not in relevance_list:
                relevance_list[item[0]] = []
            relevance_list[item[0]].append(item[1])


def calculate_precision(key: int):
    return num_of_relevant_files[key] / len(my_results_on_queries[key])


def calculate_recall(key: int):
    return num_of_relevant_files[key] / len(relevance_list[key])


def calculate_f_measure(key: int, beta: float = 0.5):
    try:
        return (beta * beta + 1) * calculate_precision(key) * calculate_recall(key) \
               / (beta * beta * calculate_precision(key) + calculate_recall(key))
    except ZeroDivisionError:
        return 0


def write_results(where_to_write_result='results/system_evaluation.txt'):
    result_string = ''
    for key in relevance_list:
        result_string += f'QUERY {key}\n'
        result_string += f'Precision = {calculate_precision(key)}\n'
        result_string += f'Recall = {calculate_recall(key)}\n'
        result_string += f'F-measure = {calculate_f_measure(key)}\n\n'
        all_precisions.append(calculate_precision(key))
        all_recalls.append(calculate_recall(key))
        all_f_measures.append(calculate_f_measure(key))

    result_string += f'Minimal precision = {min(all_precisions)}\n'
    result_string += f'Maximum precision = {max(all_precisions)}\n'
    result_string += f'Average precision = {sum(all_precisions) / len(all_precisions)}\n\n'

    result_string += f'Minimal recall = {min(all_recalls)}\n'
    result_string += f'Maximum recall = {max(all_recalls)}\n'
    result_string += f'Average recall = {sum(all_recalls) / len(all_recalls)}\n\n'

    result_string += f'Minimal F-measure = {min(all_f_measures)}\n'
    result_string += f'Maximum F-measure = {max(all_f_measures)}\n'
    result_string += f'Average F-measure = {sum(all_f_measures) / len(all_f_measures)}\n\n'

    with open(where_to_write_result, 'w') as f:
        f.write(result_string)


queries_list = parse_queries()
parse_relevance_results()
parse_files_to_str()

tokenized_corpus = [doc.split(" ") for doc in list(files_list.values())]
bm25 = BM25Okapi(tokenized_corpus)

my_results_on_queries = {}

counter = 0
for query in queries_list:
    counter += 1
    print(counter)
    tokenized_query = query.split(" ")
    res = bm25.get_top_n(tokenized_query, list(files_list.values()), n=10)

    keys = [k for k, v in files_list.items() for val in res if v == val]
    my_results_on_queries[queries_list.index(query) + 1] = keys

print()

all_precisions = []
all_recalls = []
all_f_measures = []

num_of_relevant_files = {}
for key in my_results_on_queries:
    num_of_relevant_files[key] = 0
    for item in my_results_on_queries[key]:
        if item in relevance_list[key]:
            num_of_relevant_files[key] += 1

write_results('results/system_evaluation_okapi.txt')
