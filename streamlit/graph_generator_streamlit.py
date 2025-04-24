import random
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

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
    plt.figure(figsize=(8, 8))
    if nx.get_edge_attributes(G, 'weight'):
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    else:
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
    st.pyplot(plt)

def print_adjacency_matrix(G):
    adj_matrix = nx.adjacency_matrix(G).todense()
    st.write("Adjacency Matrix:")
    st.write(adj_matrix)

def handle_random_graph():
    st.header("Generate a Random Graph")
    num_nodes = st.number_input("Enter the number of nodes", min_value=2, max_value=100, value=5)
    edge_prob = st.slider("Enter the edge creation probability (0-1)", 0.0, 1.0, 0.5)
    directed = st.checkbox("Should the graph be directed?")
    weighted = st.checkbox("Should the graph be weighted?")

    if weighted:
        min_weight = st.number_input("Enter the minimum weight", min_value=1, max_value=10, value=1)
        max_weight = st.number_input("Enter the maximum weight", min_value=1, max_value=100, value=10)
        G = generate_random_graph(num_nodes, edge_prob, directed, weighted, min_weight, max_weight)
    else:
        G = generate_random_graph(num_nodes, edge_prob, directed, weighted)

    st.subheader("Adjacency Matrix:")
    print_adjacency_matrix(G)
    draw_graph(G)  # Show the graph immediately
    return G
