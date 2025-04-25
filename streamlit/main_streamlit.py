import streamlit as st
import networkx as nx
import pandas as pd
import random

def select_shortest_path_algorithm_streamlit(G):
    """
    Streamlit version of the algorithm selector.
    """
    algo_options = [
        "Dijkstra's Algorithm",
        "Bellman-Ford Algorithm",
        "Floyd-Warshall Algorithm (All Pairs)"
    ]
    algo_choice = st.selectbox("Choose a shortest path algorithm:", algo_options)

    source = st.number_input("Source node", min_value=0, max_value=len(G.nodes) - 1, value=0)
    target = st.number_input("Target node", min_value=0, max_value=len(G.nodes) - 1, value=len(G.nodes) - 1)

    if st.button("Run Algorithm"):
        if not nx.has_path(G, source, target):
            st.error(f"No path exists between node {source} and node {target}.")
            return

        if algo_choice == "Dijkstra's Algorithm":
            path = nx.dijkstra_path(G, source, target, weight='weight')
            st.success(f"Dijkstra's Path: {path}")
        elif algo_choice == "Bellman-Ford Algorithm":
            path_dict = nx.single_source_bellman_ford_path(G, source, weight='weight')
            path = path_dict.get(target)
            if path:
                st.success(f"Bellman-Ford Path: {path}")
            else:
                st.error("No path found using Bellman-Ford.")
        elif algo_choice == "Floyd-Warshall Algorithm (All Pairs)":
            pred, dist = nx.floyd_warshall_predecessor_and_distance(G, weight='weight')
            path = []
            u = target
            while u != source:
                path.insert(0, u)
                u = pred[source].get(u)
                if u is None:
                    st.error("No path found using Floyd-Warshall.")
                    return
            path.insert(0, source)
            st.success(f"Floyd-Warshall Path: {path}")

def main_streamlit():
    """
    Streamlit main app for graph creation and algorithm selection.
    """
    st.title("📈 Graph Shortest Path Visualizer")

    mode = st.radio("Choose Graph Mode", ["Random", "User-defined"])

    G = None
    if mode == "Random":
        num_nodes = st.slider("Number of Nodes", min_value=2, max_value=20, value=5)
        prob = st.slider("Edge Probability", min_value=0.1, max_value=1.0, step=0.1, value=0.5)
        weighted = st.checkbox("Make it Weighted", value=True)

        if st.button("Generate Random Graph"):
            G = nx.erdos_renyi_graph(n=num_nodes, p=prob, directed=True)
            if weighted:
                # Assign random weights to edges
                for u, v in G.edges():
                    G[u][v]['weight'] = random.randint(1, 10)
            st.success(f"Generated Random Graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

            # Display Adjacency Matrix
            adj_matrix = nx.to_numpy_matrix(G)
            st.write("Adjacency Matrix:")
            st.dataframe(pd.DataFrame(adj_matrix))

    elif mode == "User-defined":
        st.warning("User-defined input not implemented in this version. (Want help building it?)")

    if G:
        st.graphviz_chart(nx.nx_pydot.to_pydot(G).to_string())
        select_shortest_path_algorithm_streamlit(G)

if __name__ == "__main__":
    main_streamlit()
