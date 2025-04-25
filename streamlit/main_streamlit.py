import random
import time
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

# ─── Graph generation ──────────────────────────────────────────────────────────
def generate_random_graph(n, p, directed, weighted, min_w, max_w):
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < p:
                w = random.randint(min_w, max_w) if weighted else 1
                G.add_edge(i, j, weight=w)
    return G

def draw_graph(G):
    plt.clf()
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray")
    if nx.get_edge_attributes(G, 'weight'):
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    st.pyplot(plt)

def show_adjacency(G):
    mat = nx.adjacency_matrix(G, weight="weight").todense()
    st.write(mat)

# ─── Timing helper ─────────────────────────────────────────────────────────────
def measure(func, *args, **kwargs):
    start = time.time()
    out = func(*args, **kwargs)
    return out, time.time() - start

# ─── Algorithms ────────────────────────────────────────────────────────────────
def improved_dijkstra(G, source, target):
    pq = [(0, source)]
    dist = {n: float("inf") for n in G.nodes()}
    dist[source] = 0
    prev = {n: None for n in G.nodes()}
    while pq:
        d, u = heapq.heappop(pq)
        if u == target:
            break
        for v, attr in G[u].items():
            w = attr.get("weight", 1)
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    path, u = [], target
    while u is not None:
        path.append(u)
        u = prev[u]
    return list(reversed(path)), dist[target]

def safe_dijkstra(G, s, t):
    try:
        path, tm = measure(nx.dijkstra_path, G, s, t, weight="weight")
        length = nx.dijkstra_path_length(G, s, t, weight="weight")
        return path, length, tm
    except nx.NetworkXNoPath:
        return None, None, 0.0

def safe_improved(G, s, t):
    try:
        (path, length), tm = measure(improved_dijkstra, G, s, t)
        return path, length, tm
    except nx.NetworkXNoPath:
        return None, None, 0.0

def safe_bellman(G, s, t):
    try:
        paths, tm = measure(nx.single_source_bellman_ford_path, G, s, weight="weight")
        lengths = nx.single_source_bellman_ford_path_length(G, s, weight="weight")
        return paths[t], lengths[t], tm
    except nx.NetworkXNoPath:
        return None, None, 0.0

def safe_floyd(G):
    (pred, dist), tm = measure(nx.floyd_warshall_predecessor_and_distance, G, weight="weight")
    # build all-pairs paths
    paths = {u: {} for u in G.nodes()}
    for u in G.nodes():
        for v in G.nodes():
            if u == v:
                paths[u][v] = [u]
            elif v not in pred[u]:
                paths[u][v] = None
            else:
                p = [v]
                while p[-1] != u:
                    p.append(pred[u][p[-1]])
                paths[u][v] = list(reversed(p))
    # convert distances dict-of-dicts to DataFrame-friendly
    plain_dist = {u: dict(dist[u]) for u in dist}
    return paths, plain_dist, tm

# ─── Streamlit UI ──────────────────────────────────────────────────────────────
def main():
    st.title("Graph Generator & Shortest-Path Finder")

    if "G" not in st.session_state:
        st.session_state.G = None

    # Sidebar: graph controls
    with st.sidebar:
        st.header("Graph Controls")
        kind = st.radio("Graph type", ["Random", "User-Defined"])
        if kind == "Random":
            n = st.number_input("Nodes", 1, 50, 5)
            p = st.slider("Edge prob", 0.0, 1.0, 0.3)
            directed = st.checkbox("Directed")
            weighted = st.checkbox("Weighted")
            if weighted:
                min_w = st.number_input("Min weight", 1, 1)
                max_w = st.number_input("Max weight", 1, 10)
            else:
                min_w, max_w = 1, 1
            if st.button("Generate Graph"):
                st.session_state.G = generate_random_graph(n, p, directed, weighted, min_w, max_w)
        else:
            directed = st.checkbox("Directed")
            weighted = st.checkbox("Weighted")
            text = st.text_area("Adj matrix rows (space-sep)")
            if st.button("Load Graph"):
                mat = [list(map(float, row.split())) for row in text.splitlines() if row]
                G = nx.DiGraph() if directed else nx.Graph()
                G.add_nodes_from(range(len(mat)))
                for i, row in enumerate(mat):
                    for j, w in enumerate(row):
                        if w != 0:
                            G.add_edge(i, j, weight=w)
                st.session_state.G = G

    G = st.session_state.G

    if G is None:
        st.info("Generate or load a graph first.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Graph")
        draw_graph(G)
    with col2:
        st.subheader("Adjacency Matrix")
        show_adjacency(G)

    st.subheader("Shortest-Path")
    algo = st.selectbox("Algorithm", ["Dijkstra", "Improved Dijkstra", "Bellman-Ford", "Floyd-Warshall", "Compare All"])
    s = st.number_input("Source", min_value=0, max_value=len(G)-1, value=0)
    t = st.number_input("Target", min_value=0, max_value=len(G)-1, value=1)

    result_box = st.empty()
    if st.button("Run"):
        with result_box:
            if algo == "Dijkstra":
                path, length, tm = safe_dijkstra(G, s, t)
                if path:
                    st.write(f"Path={path}, Len={length}, Time={tm:.6f}s")
                else:
                    st.error("No path")
            elif algo == "Improved Dijkstra":
                path, length, tm = safe_improved(G, s, t)
                if path:
                    st.write(f"Path={path}, Len={length}, Time={tm:.6f}s")
                else:
                    st.error("No path")
            elif algo == "Bellman-Ford":
                path, length, tm = safe_bellman(G, s, t)
                if path:
                    st.write(f"Path={path}, Len={length}, Time={tm:.6f}s")
                else:
                    st.error("No path")
            elif algo == "Floyd-Warshall":
                paths, dist, tm = safe_floyd(G)
                st.write("All-pairs distances:")
                st.dataframe(pd.DataFrame(dist))
                st.write("All-pairs paths:")
                for u, row in paths.items():
                    for v, pth in row.items():
                        st.write(f"{u}→{v}: {pth}")
                st.write(f"Time={tm:.6f}s")
            else:  # Compare All
                d_p, d_l, d_tm = safe_dijkstra(G, s, t)
                i_p, i_l, i_tm = safe_improved(G, s, t)
                b_p, b_l, b_tm = safe_bellman(G, s, t)
                _, dist, f_tm = safe_floyd(G)
                f_p = None if dist[s][t] == float('inf') else safe_floyd(G)[0][s][t]
                st.write("### Compare All Algorithms")
                st.write(f"Dijkstra: Time={d_tm:.6f}s  Path={d_p}  Len={d_l}")
                st.write(f"Improved Dijkstra: Time={i_tm:.6f}s  Path={i_p}  Len={i_l}")
                st.write(f"Bellman-Ford: Time={b_tm:.6f}s  Path={b_p}  Len={b_l}")
                st.write(f"Floyd-Warshall: Time={f_tm:.6f}s  Path={f_p}  Len={dist[s][t]}")

if __name__ == "__main__":
    main()
