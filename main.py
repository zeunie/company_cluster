from visualize_cent import centrality
from node import node_vector
from df4ssan import ssan_df
from df4rule import rule_df
from similarity import save_l2_norm, save_cos_sim
from company_cluster import company_vector, company_clustering
from cluster_visualize import cluster_on_graph
from similar_words_graph import sim_words_graph

# company names
com_list = ['amd', 'nvidia', 'qualcomm', 'samsung', 'sony', 'lucid', 'tesla', 'toyota', 'disney', 'netflix']
# com_list = ['tesla', 'sony', 'lucid']

# Choose Rule-based vs SSAN
df = rule_df(com_list)
# df = ssan_df(com_list)

# visualize graph with degree centrality and betweenness centrality
G = centrality(df)

# node2vec start
nodes_vec = node_vector(G)

# company vectors -> def company_vector(nodes_vec, com_list):
com_vec = company_vector(nodes_vec, com_list)

# (not necessary) save similarities
save_l2_norm(com_list, nodes_vec)
save_cos_sim(com_list, nodes_vec)
# (not necessary) save similar words graph using node2vec result
interest_list = ['tesla', 'sony', 'lucid']
sim_words_graph(nodes_vec, interest_list, 100)

# company clustering -> def company_clustering(com_list, com_vec, k, method):
com_cluster = company_clustering(com_list, com_vec, 4, 'gmm')

# company cluster visualizataion using pca
cluster_on_graph(com_vec, com_cluster, com_list, 'pca')

# company cluster visualizataion using tsne
cluster_on_graph(com_vec, com_cluster, com_list, 'tsne')

print("end")