import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def sim_words_df(com_name, nodes_vec, topn):
  similar_words = [nodes_vec.wv.most_similar(com_name, topn=topn)[i][0] for i in range(len(nodes_vec.wv.most_similar(com_name, topn=topn)))]
  com_root = pd.DataFrame([{'head': com_name, 'relation': 'root', 'tail': similar_words[i]} for i in range(len(similar_words))])
  return com_root

def sim_node_graph(interest_list, nodes_vec, topn=100):
  df = pd.DataFrame()
  for com_name in interest_list:
    sim_df = sim_words_df(com_name, nodes_vec, topn)
    df = pd.concat([df, sim_df], ignore_index=True)
  
  return df

def sim_words_graph(nodes_vec, interest_list, topn = 100):
  sim_df = sim_node_graph(interest_list, nodes_vec, topn=100)
  G_sim = nx.from_pandas_edgelist(sim_df, "head", "tail", edge_attr=True, create_using=nx.Graph())

  # degree
  d = dict(G_sim.degree)

  node_color = []
  for v in d.values():
    if v == 1:
      node_color.append('blue')
    elif v >= 100:
      node_color.append('green')
    else:
      node_color.append('pink')

  plt.figure(figsize=(40, 40))
  pos = nx.spring_layout(G_sim)
  nx.draw(G_sim, with_labels=True,  pos = pos, node_color = node_color, node_size = [v*50 if v > 5 else 5*50 for v in d.values()], font_size=13)
      
  # save as png
  file_name = './graph_png/sim_words_graph'
  for com_name in interest_list:
      file_name = file_name + '_' + com_name
  file_name += '.png'

  plt.savefig(file_name)