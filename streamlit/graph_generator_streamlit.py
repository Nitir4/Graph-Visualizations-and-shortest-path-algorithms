import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

# ----------- GRAPH GENERATION -----------

def generate_random_graph(num_nodes, edge_prob, directed, weighted, min_weight=1, max_weight=10):
    G = nx.DiGraph() if directed else nx.Graph()
    for i in range(num_nodes):
        G.add_node(i)
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and random.random() < edge_prob:
                if weighted:
                    weight = random.randint(min_weight, max_weight)
                    G.add_edge(i, j, weight=weight)
                else:
                    G.add_edge(i, j)
    return G

def draw_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(6, 4))
    if nx.get_edge_attributes(G, 'weight'):
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    else:
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
    st.pyplot(plt)

def print_adjacency_matrix(G):
    adj_matrix = nx.adjacency_matrix(G).todense()
    st.subheader("Adjacency Matrix")
    st.dataframe(adj_matrix)

# ----------- STREAMLIT UI HANDLERS -----------

def handle_random_graph():
    st.subheader("🎲 Generate Random Graph")
    num_nodes = st.slider("Number of nodes", min_value=2, max_value=30, value=6)
    edge_prob = st.slider("Edge creation probability", 0.0, 1.0, 0.3)
    directed = st.checkbox("Directed graph?")
    weighted = st.checkbox("Weighted graph?")
    min_weight = 1
    max_weight = 10

    if weighted:
        col1, col2 = st.columns(2)
        min_weight = col1.number_input("Min edge weight", min_value=1, max_value=100, value=1)
        max_weight = col2.number_input("Max edge weight", min_value=1, max_value=100, value=10)

    if st.button("Generate Graph"):
        G = generate_random_graph(num_nodes, edge_prob, directed, weighted, min_weight, max_weight)
        print_adjacency_matrix(G)
        draw_graph(G)
        return G

def handle_user_defined_graph():
    st.subheader("📝 Define Graph from Adjacency Matrix")
    directed = st.checkbox("Directed?", key="dir_user")
    weighted = st.checkbox("Weighted?", key="weight_user")
    num_nodes = st.number_input("Number of nodes", min_value=2, max_value=20, value=4, step=1)

    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(range(int(num_nodes)))

    st.markdown("Enter values row-by-row (space-separated):")
    matrix_input = []
    for i in range(int(num_nodes)):
        row = st.text_input(f"Row {i+1}", key=f"row_{i}")
        matrix_input.append(row)

    if st.button("Build Graph"):
        try:
            for i, row in enumerate(matrix_input):
                weights = list(map(float, row.strip().split()))
                if len(weights) != num_nodes:
                    st.error(f"Row {i+1} must have {num_nodes} values.")
                    return None
                for j, val in enumerate(weights):
                    if val != 0:
                        if weighted:
                            G.add_edge(i, j, weight=val)
                        else:
                            G.add_edge(i, j)
            print_adjacency_matrix(G)
            draw_graph(G)
            return G
        except Exception as e:
            st.error(f"Error parsing matrix: {e}")
            return None
