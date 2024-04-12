import json

from VectorSpaceModel import create_query_vector, cos_similarity
from Variables import big_collection
from Clusterisation import get_doc_vector

with open('results/result_clusters.txt', 'r') as f:
    clusters = json.loads(f.read())

with open('results/doc-term_matrix.txt', 'r') as f:
    matrix = json.loads(f.read())

query = 'i am cool'
k = 5


def search_by_clusters(query: str):
    query_vector = create_query_vector(query, matrix.keys())

    max_cos_sim = -1
    result_leader = -1

    for leader in clusters:
        cos_sim = cos_similarity(query_vector, get_doc_vector(int(leader)))
        if cos_sim > max_cos_sim:
            max_cos_sim = cos_sim
            result_leader = leader

    cos_sims_in_cluster = {int(result_leader): cos_similarity(query_vector, get_doc_vector(int(result_leader)))}
    for file_index in clusters[result_leader]:
        cos_sims_in_cluster[file_index] = cos_similarity(query_vector, get_doc_vector(file_index))

    cos_sims_in_cluster = dict(sorted(cos_sims_in_cluster.items(), key=lambda item: item[1]))
    relevant_files = list(cos_sims_in_cluster.keys())[0:k]
    return [big_collection[file_index] for file_index in relevant_files]


result = search_by_clusters(query)
print(result)
