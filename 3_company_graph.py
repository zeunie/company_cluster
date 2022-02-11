import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
#from df4ssan import company_df
from df4rule import company_re

def node_color_edge_count(com1_df, com1_name, com2_df, com2_name, com3_df, com3_name):
  com1_word = set()
  com2_word = set()
  com3_word = set()
  df_concat = pd.concat([com1_df, com2_df, com3_df], ignore_index=True)

  for i in range(len(com1_df)):
    com1_word.add(com1_df['head'][i])
    com1_word.add(com1_df['tail'][i])

  for i in range(len(com2_df)):
    com2_word.add(com2_df['head'][i])
    com2_word.add(com2_df['tail'][i])

  for i in range(len(com3_df)):
    com3_word.add(com3_df['head'][i])
    com3_word.add(com3_df['tail'][i])

  # create graph
  G = nx.from_pandas_edgelist(df_concat, "head", "tail", 
                          edge_attr=True, edge_key="company_name", create_using=nx.Graph())
  
# ------- node color ------------------------------------------------------------
  # Making a color list
  node_lst = list(G.nodes)
  node_color = []

  for i in range(len(node_lst)):
    # 회사명은 중복을 고려하지 않음
    if (node_lst[i] == com1_name):
      # com1
      node_color.append('blue')
    # com2
    elif (node_lst[i] == com2_name):
      node_color.append('red')
    # com3
    elif (node_lst[i] == com3_name):
      node_color.append('yellow')

    # 세 개 모두
    elif (node_lst[i] in com1_word and node_lst[i] in com2_word and node_lst[i] in com3_word):
      node_color.append('pink')
    # com1, com2
    elif (node_lst[i] in com1_word and node_lst[i] in com2_word):
      node_color.append('purple')
    # com1, com3
    elif (node_lst[i] in com1_word and node_lst[i] in com3_word):
      node_color.append('green')
    # com2, com3
    elif (node_lst[i] in com2_word and node_lst[i] in com3_word):
      node_color.append('orange')
    # com1 only
    elif node_lst[i] in com1_word:
      node_color.append('blue')
    # com2 only
    elif node_lst[i] in com2_word:
      node_color.append('red')
    # com3 only
    else:
      node_color.append('yellow')

# ---------------- edge count -------------------------------------------------------------
  # count the edge
  edge_lst = list(G.edges)
  edge_cnt = []

  for i in range(len(edge_lst)):
    cnt = 0

    for j in range(len(df_concat)):
      # (A, B)와 (B, A)처럼 순서가 바뀌는 경우 고려
      if (edge_lst[i] == (df_concat['head'][j], df_concat['tail'][j]) or edge_lst[i] == (df_concat['tail'][j], df_concat['head'][j])):
        cnt += 1
    
    edge_cnt.append(cnt)

  # match the format
  dict_weight = {}
  for i in range(len(edge_lst)):
    dict_weight[edge_lst[i]] = dict(weight = edge_cnt[i])
  nx.set_edge_attributes(G, dict_weight)

  return G, node_color

def main():
    tesla_df = company_re('tesla')
    sony_df = company_re('sony')
    lucid_df = company_re('lucid')

    G, node_color = node_color_edge_count(tesla_df, 'tesla', sony_df, 'sony', lucid_df, 'lucid')
    
    # degree
    d = dict(G.degree)

    #visualize
    plt.figure(figsize=(50, 50))
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color = node_color,  pos = pos, node_size = [v * 100 for v in d.values()], font_size=15)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    # plt.show()
    plt.savefig("./graph_png/3_company.png")

if __name__ == "__main__":
    main()