import json

with open('results/result.txt', 'r') as f:
    dictionary = json.loads(f.read())


class Node:
    def __init__(self):
        self.nodes = {}
        self.is_end = False


class Tree:
    def __init__(self):
        self.root = Node()
        self.is_end = False

    def add_word(self, word: str):
        current_node = self.root
        for i in range(len(word)):
            if word[i] not in current_node.nodes:
                current_node.nodes[word[i]] = Node()
                current_node.nodes[word[i]].name = word[i]
            current_node = current_node.nodes[word[i]]
            if i == len(word) - 1:
                current_node.is_end = True

    def find_node(self, query: str):
        current_node = self.root
        for char in query:
            if char in current_node.nodes.keys():
                current_node = current_node.nodes[char]
        return current_node


def build_prefix_tree():
    tree = Tree()
    for word in dictionary:
        tree.add_word(word)

