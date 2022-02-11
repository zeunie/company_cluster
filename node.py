from node2vec import Node2Vec

def node_vector(G):
    node2vec = Node2Vec(graph=G, # target graph
                        dimensions=50, # embedding dimension
                        walk_length=10, # number of nodes in each walks 
                        p = 1, # return hyper parameter
                        q = 2, # inout parameter, q값을 작게 하면 structural equivalence를 강조하는 형태로 학습됩니다. 
                        weight_key='weight', # if weight_key in attrdict 
                        num_walks=2000, 
                        workers=1,
                    )

    nodes_vec = node2vec.fit(window=2)

    '''
    # 대략 walk들이 어떻게 발생하는지를 아래처럼 볼 수도 있습니다. 
    for i, each_walk in enumerate(node2vec.walks):
        print(f"{i:0>2d}, {each_walk}")
        if i>1:
            break
    '''

    return nodes_vec 