import json
import pickle
from PrefixSearhTree import Node, Tree

with open('results/result.txt', 'r') as f:
    dictionary = json.loads(f.read())

with open('results/permuterm_index.txt', 'rb') as f:
    tree = pickle.load(f)


def create_permuterm_list(word: str):
    result = []
    with_dollar = word + '$'
    result.append(with_dollar)

    while with_dollar[0] != '$':
        with_dollar = with_dollar[1:] + with_dollar[0]
        result.append(with_dollar)

    return result


def process_query_with_one_wildcard(query: str):
    query += '$'
    while query[0] != '*':
        query = query[1:] + query[0]
    return query[1:]


def wildcard_search(query: str):
    result = []
    query = process_query_with_one_wildcard(query)
    node = tree.find_node(query)
    iterating(query, node, result)
    return [to_normal_form(word) for word in result]


def iterating(word: str, current_node: Node, result: list):
    if current_node.is_end:
        result.append(word)
        return
    else:
        for node in current_node.nodes.keys():
            iterating(word + node, current_node.nodes[node], result)


def to_normal_form(with_dollar: str):
    return with_dollar.split('$', 1)[1] + with_dollar.split('$', 1)[0]


def create_permuterm_index(where_to_write_result: str = 'results/permuterm_index.txt'):
    tree = Tree()

    for word in dictionary:
        permuterm_list = create_permuterm_list(word)
        for item in permuterm_list:
            tree.add_word(item)

    with open(where_to_write_result, 'wb') as file:
        pickle.dump(tree, file)
        print(f'Object successfully saved to "{where_to_write_result}"')

    return tree


print(wildcard_search('m*n'))
print(wildcard_search('*nue'))
