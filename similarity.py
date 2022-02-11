import numpy as np
import pandas as pd
from numpy.linalg import norm

# cosine similarity
def cos_sim(com1_name, com2_name, nodes_vec):
  com1_vec = nodes_vec.wv[com1_name]
  com2_vec = nodes_vec.wv[com2_name]
  return np.dot(com1_vec, com2_vec)/(norm(com1_vec)*norm(com2_vec))

# l2 norm calculation
def l2_norm(com1_name, com2_name, nodes_vec):
  return norm(nodes_vec.wv[com1_name] - nodes_vec.wv[com2_name])

# save l2_norm
def save_l2_norm(com_list, nodes_vec):
    l2_df = pd.DataFrame(index=com_list)

    for com1 in com_list:
        # l2_df[com1] = [l2_sim(com1, com2, nodes_vec).round(3) if l2_sim(com1, com2, nodes_vec) > 0.4 else None for com2 in com_list]
        l2_df[com1] = [l2_norm(com1, com2, nodes_vec).round(3) for com2 in com_list]
    
    l2_df.to_csv('./similarity_result/l2_norm_rule.csv', mode='w')


# save cosine similarity
def save_cos_sim(com_list, nodes_vec):
    cos_df = pd.DataFrame(index=com_list)

    for com1 in com_list:
        # cos_df[com1] = [cos_sim(com1, com2, nodes_vec).round(3) if cos_sim(com1, com2, nodes_vec) > 0.4 else None for com2 in com_list]
        cos_df[com1] = [cos_sim(com1, com2, nodes_vec).round(3) for com2 in com_list]
    
    cos_df.to_csv('./similarity_result/cosine_similarity_rule.csv', mode='w')