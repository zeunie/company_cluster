from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import pandas as pd

# get company vectors
def company_vector(nodes_vec, com_list):
  com_vec = []
  for company in com_list:
    com_vec.append(nodes_vec.wv[company])
  return com_vec

def company_clustering(com_list, com_vec, k, method):
  # Data Scaling
  scaler = MinMaxScaler()
  com_scale = scaler.fit_transform(com_vec)

  if method.lower() == 'gmm':
    gmm = GaussianMixture(n_components=k, random_state=0).fit(com_vec)
    com_cluster = pd.DataFrame()
    com_cluster['cluster'] = gmm.predict(com_scale)
    com_cluster['company vector'] = com_vec
    com_cluster['company name'] = com_list

  elif method.lower() == 'kmeans':
    kmeans = KMeans(n_clusters = k, random_state=10).fit(com_vec)
    com_cluster = pd.DataFrame()
    com_cluster['cluster'] = kmeans.fit_predict(com_scale)
    com_cluster['company vector'] = com_vec
    com_cluster['company name'] = com_list
  
  return com_cluster