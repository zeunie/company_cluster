import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def cluster_on_graph(com_vec, com_cluster, com_list, method):
    #default two dimension (also can visualize three dimension)
    dimension = 2
    if method.lower() == 'pca':
        com_df = pd.DataFrame(com_vec, index = com_list)

        # Computing the correlation matrix
        X_corr = com_df.corr()

        # Computing eigen values and eigen vectors
        values, vectors = np.linalg.eig(X_corr)

        # Sorting the eigen vectors corresponding to eigen values in descending order
        args = (-values).argsort()
        values = vectors[args]
        vectors = vectors[:, args]

        # Taking first 2 components which explain maximum variance for projecting
        new_vectors = vectors[:, :dimension]

        # Projecting it onto new dimension with 2 axis
        neww_X = np.dot(com_vec, new_vectors)

        # Plotting 

        # color list
        color_lst = []
        for i in range(len(com_cluster)):
            if com_cluster['cluster'][i] == 0:
                color_lst.append('blue')
            elif com_cluster['cluster'][i] == 1:
                color_lst.append('red')
            elif com_cluster['cluster'][i] == 2:
                color_lst.append('yellow')
            elif com_cluster['cluster'][i] == 3:
                color_lst.append('black')
            elif com_cluster['cluster'][i] == 4:
                color_lst.append('pink')
            elif com_cluster['cluster'][i] == 5:
                color_lst.append('purple')
            else:
                color_lst.append('orange')

        plt.figure(figsize=(13,7))
        plt.scatter(neww_X[:,0], neww_X[:,1], linewidths=10, color=color_lst)
        plt.xlabel("PC1", size=15)
        plt.ylabel("PC2", size=15)
        plt.title("Company Embedding Space", size=20)
        vocab=list(com_list)
        for i, word in enumerate(vocab):
            plt.annotate(word, xy=(neww_X[i,0],neww_X[i,1]))

        plt.savefig("./graph_png/company_cluster_rule_pca.png")

    elif method.lower() == 'tsne':
        # t-SNE
        tsne = TSNE(n_components=dimension, verbose=1, perplexity=2, n_iter=300)
        tsne_results = tsne.fit_transform(com_vec)

        # color list
        color_lst = []
        for i in range(len(com_cluster)):
            if com_cluster['cluster'][i] == 0:
                color_lst.append('blue')
            elif com_cluster['cluster'][i] == 1:
                color_lst.append('red')
            elif com_cluster['cluster'][i] == 2:
                color_lst.append('yellow')
            elif com_cluster['cluster'][i] == 3:
                color_lst.append('black')
            elif com_cluster['cluster'][i] == 4:
                color_lst.append('pink')
            elif com_cluster['cluster'][i] == 5:
                color_lst.append('purple')
            else:
                color_lst.append('orange')
        
        plt.figure(figsize=(13,7))
        plt.scatter(tsne_results[:,0], tsne_results[:,1], linewidths=10, color=color_lst)
        plt.xlabel("tsne-2d-one", size=15)
        plt.ylabel("tsne-2d-two", size=15)
        plt.title("Company Embedding Space", size=20)
        vocab=list(com_list)
        for i, word in enumerate(vocab):
            plt.annotate(word, xy=(tsne_results[i,0],tsne_results[i,1]))
        
        plt.savefig("./graph_png/company_cluster_rule_tsne.png")