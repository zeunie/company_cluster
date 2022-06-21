# RE results graph visualization and company clustering
Winter Intern Project at KAIST Applied Artificial Intelligence Lab  
Junhyeok Jung(KAIST), Kwanghyeon Lee(KAIST), Jiwoo Shin(KAIST), Jieun Han(HUFS)


### Installation

1. pip install -r requirements.txt

2. python -m nltk.downloader stopwords 

3. python3.7 main.py



## 1. Paragraph-Level Relation Extraction using rule-based and SSAN

|- df4rule.py

 * Prerequiste
   + You need csv files that are generated with finiancial_news_api
   + Those files should be located in "visualization_code/rule_base_datasets/*.csv"

 * This code extracts relations with rule-based patterns.
   + (S + V + O) -> (head: S, relation: V, tail: O )

|- df4ssan.py

+ Prerequiste
  + We recommend you run SSAN independently, and make sure all relation extraction.json file from SSAN code saved in "output/*/SSAN_result_all_relation.json"
+ This code convert json file to dataframe and concat all the dataframes from various companies.

​	



## 2. Graph visualization by degree and betweeness centrality using networkx

|- visualize_cent.py  

* output
  + degree_centrality: "./graph_png/degree.png"
  + betweenness_centrality: "./graph_png/between.png"



## 3. Get embedding vector with Node2vec Company clustering with K-means and GMM

|- node.py

|-similarity.py

* output
  * consine similarity: "./similarity_result/consine_similarity.csv"
  * l2 norm: "./similarity_result/l2_norm.csv"

|- company_cluster.py

- GMM (soft clustering)  k: number of clusters

  **main.py**	company_clustering(com_list, com_vec, 4, **'gmm'**)

- K-means (hard clustering)

  **main.py**	company_clustering(com_list, com_vec, 4, **'kmeans'**)



​	

## 4. Visualize with PCA and TSNE

|-cluster_visualize.py 

* output
  * PCA: "./graph_png/company_cluster_pca.png"
  * TSNE: "./graph_png/company_cluster_tsne.png"



## Output

* degree_centrality: "./graph_png/degree.png"
* betweenness_centrality: "./graph_png/between.png"
* consine similarity: "./similarity_result/consine_similarity.csv"
* l2 norm: "./similarity_result/l2_norm.csv"
* PCA: "./graph_png/company_cluster_pca.png"
* TSNE: "./graph_png/company_cluster_tsne.png"
