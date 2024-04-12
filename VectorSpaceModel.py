import json
from math import sqrt
import numpy as np
from Utils import delete_punctuation


def dot_product(vector):
    result = []
    for j in range(len(vector[0])):
        col = []
        for i in range(len(vector)):
            col.append(vector[i][j])
        prod_col = np.prod(col)
        result.append(prod_col)
    sum_dot_product = np.sum(result)

    return sum_dot_product


def euclidean_length(vector):
    result = 0
    for num in vector:
        result += num * num
    return sqrt(result)


def cos_similarity(vector1, vector2):
    return np.dot(vector1, vector2) / (euclidean_length(vector1) * euclidean_length(vector2))


def create_query_vector(query: str, terms):
    return [1 if term in query else 0 for term in terms]
