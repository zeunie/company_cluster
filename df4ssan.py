import json
import pandas as pd
import os, sys 

#Run SSAN
#os.system("cd..")
#os.system("python3.7 main.py --name_companies AMZN FB --start_date 2020 6 30 --end_date 2021 6 30")

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

# load json result file
def company_df(com_name):
  com_name = com_name.lower()
  file_path = '/home/bears0013/AAILab SSAN_jieun/AAILab SSAN test/output/' + com_name + '/SSAN_result_all_relation.json'
  with open(file_path) as json_file:
    com_data = json.load(json_file)

  com_df = json2df(com_data, com_name)
  com_root = pd.DataFrame([{'head': com_name, 'relation': 'root', 'tail': com_df['head'][i]} for i in range(len(com_df)) if com_df['head'][i].lower() != com_name])
  com_df = pd.concat([com_df, com_root], ignore_index=True)

  save_path = '/home/bears0013/AAILab SSAN_jieun/AAILab SSAN test/output/' + com_name + '/ssan_re_' + com_name + '.csv'
  com_df.to_csv(save_path)
  
  return com_df

def ssan_df(com_list):
    df = pd.DataFrame()

    for com_name in com_list:
        com_df = company_df(com_name)
        df = pd.concat([df, com_df], ignore_index=True)
        
    return df