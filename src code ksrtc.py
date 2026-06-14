import networkx as nx
import matplotlib.pyplot as plt
import heapq
import math

# -------------------------
# Graph Data
# -------------------------
edges = [("TVM", "KLM", 1
          65),("TVM", "ALP", 236),("KLM", "ALP", 85),("ALP", "EKM", 60),("EKM", "TSR", 80),("TSR", "PKD", 70),("ALP", "TSR", 140),("KLM", "EKM", 130)]

cities = ["TVM","KLM","ALP","EKM","TSR","PKD"]

# -------------------------
# Create Graph
# -------------------------
G = nx.Graph()

for u,v,w in edges:
    G.add_edge(u,v,weight=w)

# -------------------------
# Dijkstra Algorithm
# -------------------------
def dijkstra(graph,start):

    dist = {node: math.inf for node in graph}
    prev = {node: None for node in graph}

    dist[start] = 0

    pq = [(0,start)]

    while pq:

        current_dist,u = heapq.heappop(pq)

        for v,data in graph[u].items():

            weight = data['weight']

            if dist[u] + weight < dist[v]:

                dist[v] = dist[u] + weight
                prev[v] = u
                heapq.heappush(pq,(dist[v],v))

    return dist,prev


def get_path(prev,target):

    path=[]

    while target:
        path.append(target)
        target = prev[target]

    return path[::-1]


# Run Dijkstra
dist,prev = dijkstra(G,"TVM")

path = get_path(prev,"PKD")

print("Shortest Path:",path)
print("Total Distance:",dist["PKD"],"km")

# -------------------------
# Floyd Warshall
# -------------------------

n=len(cities)
index={city:i for i,city in enumerate(cities)}

dist_matrix=[[math.inf]*n for _ in range(n)]

for i in range(n):
    dist_matrix[i][i]=0

for u,v,w in edges:
    i=index[u]
    j=index[v]
    dist_matrix[i][j]=w
    dist_matrix[j][i]=w


for k in range(n):
    for i in range(n):
        for j in range(n):

            dist_matrix[i][j] = min(dist_matrix[i][j],
                                    dist_matrix[i][k]+dist_matrix[k][j])

print("\nFloyd Warshall Distance Matrix")

for row in dist_matrix:
    print(row)

# -------------------------
# Visualization
# -------------------------

pos = nx.spring_layout(G)

edge_labels = nx.get_edge_attributes(G,'weight')

plt.figure(figsize=(8,6))

nx.draw(G,pos,
        with_labels=True,
        node_color='lightblue',
        node_size=2000,
        font_size=10)

nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)

# Highlight shortest path
path_edges=list(zip(path,path[1:]))

nx.draw_networkx_edges(G,pos,
                       edgelist=path_edges,
                       width=4,
                       edge_color='red')

plt.title("KSRTC Route Optimization Graph\n(Red = Shortest Path)")
plt.show()