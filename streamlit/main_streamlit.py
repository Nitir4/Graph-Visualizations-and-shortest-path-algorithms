import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import pandas as pd

# Set Streamlit config
st.set_page_config(page_title="Graph Algorithms Visualizer", layout="wide")

# ----------------------------
# Utility functions
# ----------------------------

def generate_random_graph(n, p=0.3):
    G = nx.erdos_renyi_graph(n, p, directed=False)
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(n, p, directed=False)
    for (u, v) in G.edges():
        G[u][v]['weight'] = random.randint(1, 10)
    return G

def draw_graph(G, path=None):
    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    plt.figure(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=700, font_size=14)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange')

    st.pyplot(plt.gcf())
    plt.clf()

def measure(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return result, end - start

# ----------------------------
# Algorithms
# ----------------------------

def safe_dijkstra(G, s, t):
    try:
        path, time_ = measure(nx.dijkstra_path, G, s, t, weight='weight')
        length = nx.dijkstra_path_length(G, s, t, weight='weight')
        return path, length, time_
    except:
        return None, None, 0

def safe_bellman_ford(G, s, t):
    try:
        path, time_ = measure(nx.bellman_ford_path, G, s, t, weight='weight')
        length = nx.bellman_ford_path_length(G, s, t, weight='weight')
        return path, length, time_
    except:
        return None, None, 0

def safe_floyd(G):
    (pred, dist), tm = measure(nx.floyd_warshall_predecessor_and_distance, G, weight="weight")
    paths = {}
    for u in G.nodes():
        paths[u] = {}
        for v in G.nodes():
            if u == v or v not in pred[u]:
                paths[u][v] = [u] if u == v else None
            else:
                path = [v]
                while path[-1] != u:
                    path.append(pred[u][path[-1]])
                paths[u][v] = list(reversed(path))
    plain_dist = {u: dict(dist[u]) for u in dist}
    return paths, plain_dist, tm

def safe_floyd_single(G, s, t):
    paths, dist, tm = safe_floyd(G)
    return paths[s][t], dist[s][t], tm

# ----------------------------
# Main App
# ----------------------------

def main():
    st.title("📊 Graph Visualizer & Shortest Path Finder")

    if 'graph' not in st.session_state:
        st.session_state.graph = generate_random_graph(6)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Generate New Graph"):
            st.session_state.graph = generate_random_graph(6)

    G = st.session_state.graph
    st.subheader("Graph")
    draw_graph(G)

    st.subheader("Adjacency Matrix")
    adj = nx.to_pandas_adjacency(G, dtype=int)
    st.dataframe(adj)

    nodes = list(G.nodes())
    s = st.selectbox("Source Node", nodes, key="source")
    t = st.selectbox("Target Node", nodes, key="target")

    algo = st.selectbox("Choose Algorithm", ["Dijkstra", "Bellman-Ford", "Floyd-Warshall", "Compare All"])

    st.markdown("---")

    if algo == "Dijkstra":
        path, length, tm = safe_dijkstra(G, s, t)
        st.subheader("Dijkstra's Algorithm")
        draw_graph(G, path)
        if path:
            st.write(f"Path: {path}")
            st.write(f"Cost: {length}")
        else:
            st.warning("No path found.")
        st.write(f"Time Elapsed: {tm:.6f}s")

    elif algo == "Bellman-Ford":
        path, length, tm = safe_bellman_ford(G, s, t)
        st.subheader("Bellman-Ford Algorithm")
        draw_graph(G, path)
        if path:
            st.write(f"Path: {path}")
            st.write(f"Cost: {length}")
        else:
            st.warning("No path found.")
        st.write(f"Time Elapsed: {tm:.6f}s")

    elif algo == "Floyd-Warshall":
        st.subheader("Floyd-Warshall Algorithm")
        paths, dist, tm = safe_floyd(G)
        st.write("All-Pairs Distance Matrix:")
        st.dataframe(pd.DataFrame(dist).astype(int))
        st.write("All-Pairs Paths:")
        for u in paths:
            for v in paths[u]:
                st.write(f"{u} → {v}: {paths[u][v]}")
        st.write(f"Time Elapsed: {tm:.6f}s")

    elif algo == "Compare All":
        st.subheader("⏱ Compare All Algorithms")
        d_path, d_len, d_tm = safe_dijkstra(G, s, t)
        b_path, b_len, b_tm = safe_bellman_ford(G, s, t)
        f_path, f_len, f_tm = safe_floyd_single(G, s, t)

        st.write(f"**Dijkstra** → Time: `{d_tm:.6f}s` | Path: `{d_path}` | Cost: `{d_len}`")
        st.write(f"**Bellman-Ford** → Time: `{b_tm:.6f}s` | Path: `{b_path}` | Cost: `{b_len}`")
        st.write(f"**Floyd-Warshall** → Time: `{f_tm:.6f}s` | Path: `{f_path}` | Cost: `{f_len}`")

if __name__ == "__main__":
    main()
