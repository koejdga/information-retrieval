import json
import random
from math import sqrt
from Variables import big_collection
from VectorSpaceModel import cos_similarity
from InvertedIndex import create_an_incidence_matrix
from Utils import final_processing


def get_doc_vector(file_index):
    return [matrix[word][file_index] for word in matrix]


def create_clusters(file_collection: list, where_to_write_result: str = 'results/result_clusters.txt'):
    result_clusters = {}
    leaders = random.sample(range(0, len(file_collection)), int(sqrt(len(file_collection))))
    leader_vectors = {}

    for leader in leaders:
        result_clusters[leader] = []
        leader_vectors[leader] = get_doc_vector(leader)

    for file in file_collection:
        if file_collection.index(file) not in leaders:
            doc_vector = get_doc_vector(file_collection.index(file))
            max_cos_similarity = 0
            cluster_num = -1
            for leader in leaders:
                cos_sim = cos_similarity(doc_vector, leader_vectors[leader])

                if cos_sim > max_cos_similarity:
                    cluster_num = leader
                    max_cos_similarity = cos_sim

            result_clusters[cluster_num].append(file_collection.index(file))

    final_processing(result_clusters, where_to_write_result, 'clusters')
    return result_clusters


with open('results/doc-term_matrix.txt', 'r') as f:
    matrix = json.loads(f.read())
# clusters = create_clusters(big_collection[0:300])

with open('results/result_clusters.txt', 'r') as f:
    clusters = json.loads(f.read())
print(clusters)
