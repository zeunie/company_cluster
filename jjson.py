import pandas as pd
import json
import networkx as nx
import matplotlib.pyplot as plt


# Making json file to dataframe function
def json2df(json_data, com_name):
  # Making each column list
  head_list = []
  relation_list = []
  tail_list = []
  company_list = []

  for i in range(len(json_data)):
    head_list.append(json_data[i]['head'].lower())
    relation_list.append(json_data[i]['relation'])
    tail_list.append(json_data[i]['tail'].lower())
    company_list.append(com_name)

  # Making dataframe using above lists
  head_dict = {'head': head_list}
  df = pd.DataFrame(head_dict)
  df['relation'] = relation_list
  df['tail'] = tail_list
  df['company_name'] = company_list

  return df



