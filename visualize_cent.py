import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def centrality(df):
    G = nx.from_pandas_edgelist(df, "head", "tail", 
                        edge_attr=True, create_using=nx.Graph())

    # edge count
    edge_lst = list(G.edges)
    edge_cnt = []

    for i in range(len(edge_lst)):
        cnt = 0
        for j in range(len(df)):
            # (A, B)와 (B, A)처럼 순서가 바뀌는 경우 고려
            if (edge_lst[i] == (df['head'][j], df['tail'][j]) or edge_lst[i] == (df['tail'][j], df['head'][j])):
                cnt += 1

        edge_cnt.append(cnt)

    # match the format
    dict_weight = {}
    for i in range(len(edge_lst)):
        dict_weight[edge_lst[i]] = dict(weight = edge_cnt[i])
    nx.set_edge_attributes(G, dict_weight)
    
    # degree
    d = dict(G.degree)

    #visualize
    plt.figure(figsize=(50, 50))
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True,  pos = pos, node_size = [v * 100 for v in d.values()], font_size=15)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # betweenness
    btw_cen = nx.betweenness_centrality(G, endpoints=True)

    #visualize
    plt.figure(figsize=(50, 50))
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, pos = pos, node_size = [v * 15000 for v in btw_cen.values()], font_size=15)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    # plt.show()
    plt.savefig("./graph_png/degree_rule.png")

    # plt.show()
    plt.savefig("./graph_png/between_rule.png")
    
    return G
