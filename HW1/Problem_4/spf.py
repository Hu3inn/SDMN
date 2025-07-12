import networkx as nx

def Cost2Edge(Cost_mat, Edge_list):
    N = len(Cost_mat)
    for j in range(N):
        for i in range(N):
            if Cost_mat[j][i] != 0:
                Edge_list.append((j + 1, i + 1, Cost_mat[j][i]))     
    return Edge_list            
                        
def best_Path(Cost_matrix, src, dst):   
    G = nx.DiGraph()
    elist = []
    elist = Cost2Edge(Cost_matrix, elist)
    G.add_weighted_edges_from(elist)
    return {
        "send": list(nx.dijkstra_path(G, source=src, target=dst)),
        "receive": list(nx.dijkstra_path(G, source=dst, target=src))
    }