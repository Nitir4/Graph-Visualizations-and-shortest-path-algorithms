import random
import time
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import streamlit as st

st.set_page_config(layout="wide")

# ─── Graph generation ──────────────────────────────────────────────────────────
def generate_random_graph(num_nodes, edge_prob, directed, weighted, min_w, max_w):
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(range(num_nodes))
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i!=j and random.random() < edge_prob:
                w = random.randint(min_w, max_w) if weighted else 1
                G.add_edge(i, j, weight=w)
    return G

def draw_graph(G):
    plt.clf()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray")
    if nx.get_edge_attributes(G,'weight'):
        nx.draw_networkx_edge_labels(G,pos,
            edge_labels=nx.get_edge_attributes(G,'weight'))
    st.pyplot(plt)

def show_adjacency(G):
    mat = nx.adjacency_matrix(G, weight='weight').todense()
    st.write(mat)

# ─── Shortest-path wrappers ─────────────────────────────────────────────────────
def measure(func, *args):
    start = time.time()
    out = func(*args)
    return out, time.time()-start

def safe_dijkstra(G,s,t):
    try:
        path, time_ = measure(nx.dijkstra_path, G, s, t, weight='weight')
        length = nx.dijkstra_path_length(G, s, t, weight='weight')
        return path, length, time_
    except nx.NetworkXNoPath:
        return None, None, None

def safe_improved(G,s,t):
    try:
        (path, length), time_ = measure(improved_dijkstra_impl, G, s, t)
        return path, length, time_
    except nx.NetworkXNoPath:
        return None, None, None

def safe_bellman(G,s,t):
    try:
        paths, time_ = measure(nx.single_source_bellman_ford_path, G, s, weight='weight')
        lengths = nx.single_source_bellman_ford_path_length(G, s, weight='weight')
        return paths[t], lengths[t], time_
    except nx.NetworkXNoPath:
        return None, None, None

def safe_floyd(G, s, t):
    # floyd_warshall returns dict-of-dicts of distances
    dist, time_ = measure(nx.floyd_warshall, G, weight='weight')
    # no explicit path reconstruction here
    return dist, time_

def improved_dijkstra_impl(G, source, target):
    # priority-queue based Dijkstra
    pq = [(0,source)]
    dist = {n:float('inf') for n in G.nodes()}
    dist[source]=0
    prev={n:None for n in G.nodes()}
    while pq:
        d,u = heapq.heappop(pq)
        if u==target: break
        for v,attr in G[u].items():
            w = attr.get('weight',1)
            nd = d+w
            if nd<dist[v]:
                dist[v]=nd
                prev[v]=u
                heapq.heappush(pq,(nd,v))
    # reconstruct
    path=[]
    u=target
    while u is not None:
        path.append(u)
        u=prev[u]
    path.reverse()
    return path, dist[target]

# ─── Streamlit UI ──────────────────────────────────────────────────────────────
def main():
    st.title("📊 Graph & Shortest-Path Visualizer")

    # initialize
    if 'G' not in st.session_state:
        st.session_state.G = None

    # Graph controls
    with st.sidebar:
        st.header("Graph Controls")
        kind = st.radio("Graph type", ["Random", "User-Defined"])
        if kind=="Random":
            n = st.number_input("Nodes", min_value=1, value=5)
            p = st.slider("Edge probability", 0.0, 1.0, 0.3)
            directed = st.checkbox("Directed")
            weighted = st.checkbox("Weighted")
            if weighted:
                min_w = st.number_input("Min weight", value=1)
                max_w = st.number_input("Max weight", value=10)
            else:
                min_w, max_w = 1,1
            if st.button("Generate Graph"):
                st.session_state.G = generate_random_graph(n,p,directed,weighted,min_w,max_w)
        else:
            directed = st.checkbox("Directed")
            weighted = st.checkbox("Weighted")
            rows = st.text_area("Adjacency matrix (rows of space-sep weights)")
            if st.button("Load Graph"):
                mat = [list(map(float,row.split())) for row in rows.splitlines() if row]
                G = nx.DiGraph() if directed else nx.Graph()
                size = len(mat)
                G.add_nodes_from(range(size))
                for i in range(size):
                    for j,w in enumerate(mat[i]):
                        if w!=0: G.add_edge(i,j,weight=w)
                st.session_state.G = G

    G = st.session_state.G

    # Display graph & matrix
    if G is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Graph")
            draw_graph(G)
        with col2:
            st.subheader("Adjacency Matrix")
            show_adjacency(G)

        # Shortest-path controls
        st.subheader("Shortest-Path Algorithms")
        algo = st.selectbox("Algorithm", ["Dijkstra","Improved","Bellman-Ford","Floyd-Warshall","Compare All"])
        s = st.number_input("Source", min_value=0, max_value=len(G)-1, value=0)
        t = st.number_input("Target", min_value=0, max_value=len(G)-1, value=1)
        if st.button("Run"):
            if algo=="Dijkstra":
                path,length,tm = safe_dijkstra(G,s,t)
                if path is None: st.error("No path!")
                else: st.write(f"Path: {path}  Length: {length}  Time: {tm:.6f}s")
            elif algo=="Improved":
                path,length,tm = safe_improved(G,s,t)
                if path is None: st.error("No path!")
                else: st.write(f"Path: {path}  Length: {length}  Time: {tm:.6f}s")
            elif algo=="Bellman-Ford":
                path,length,tm = safe_bellman(G,s,t)
                if path is None: st.error("No path!")
                else: st.write(f"Path: {path}  Length: {length}  Time: {tm:.6f}s")
            elif algo=="Floyd-Warshall":
                dist,tm = safe_floyd(G,s,t)
                st.write(f"All-pairs distances:\n {dist}\nTime: {tm:.6f}s")
            else:  # Compare All
                st.write("## Compare All Algorithms")
                for name,fn in [("Dijkstra", safe_dijkstra),
                                ("Improved", safe_improved),
                                ("Bellman-Ford", safe_bellman),
                                ("Floyd-Warshall", safe_floyd)]:
                    if name=="Floyd-Warshall":
                        dist,tm = fn(G,s,t)
                        st.write(f"**{name}** time: {tm:.6f}s")
                    else:
                        path,length,tm = fn(G,s,t)
                        if path is None:
                            st.write(f"**{name}**: No path")
                        else:
                            st.write(f"**{name}**: Path={path}, Len={length}, Time={tm:.6f}s")

    else:
        st.info("Generate or load a graph first.")

if __name__=="__main__":
    main()
