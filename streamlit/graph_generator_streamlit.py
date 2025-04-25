import networkx as nx
import random
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
    if nx.get_edge_attributes(G, 'weight'):
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    else:
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
    plt.show()

def handle_random_graph():
    st.title("Random Graph Generation")
    num_nodes = st.number_input("Enter the number of nodes", min_value=2, max_value=100, value=10)
    edge_prob = st.slider("Enter the edge creation probability", min_value=0.0, max_value=1.0, value=0.2)
    directed = st.checkbox("Should the graph be directed?")
    weighted = st.checkbox("Should the graph be weighted?")
    
    if weighted:
        min_weight = st.number_input("Enter the minimum weight", min_value=1, value=1)
        max_weight = st.number_input("Enter the maximum weight", min_value=1, value=10)
        G = generate_random_graph(num_nodes, edge_prob, directed, weighted, min_weight, max_weight)
    else:
        G = generate_random_graph(num_nodes, edge_prob, directed, weighted)
    
    st.subheader("Adjacency Matrix:")
    adj_matrix = nx.adjacency_matrix(G).todense()
    st.write(adj_matrix)
    
    st.subheader("Graph Visualization:")
    draw_graph(G)
    return G

def handle_user_defined_graph():
    st.title("User Defined Graph")
    directed = st.checkbox("Should the graph be directed?")
    weighted = st.checkbox("Should the graph be weighted?")
    num_nodes = st.number_input("Enter the number of nodes", min_value=2, max_value=100, value=5)
    
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(range(num_nodes))
    
    adj_matrix_str = st.text_area("Enter the adjacency matrix row by row (space-separated values):", height=200)
    rows = adj_matrix_str.strip().split("\n")
    for i, row in enumerate(rows):
        weights = list(map(float, row.strip().split()))
        for j, weight in enumerate(weights):
            if weight != 0:
                if weighted:
                    G.add_edge(i, j, weight=weight)
                else:
                    G.add_edge(i, j)
    
    st.subheader("Adjacency Matrix:")
    adj_matrix = nx.adjacency_matrix(G).todense()
    st.write(adj_matrix)
    
    st.subheader("Graph Visualization:")
    draw_graph(G)
    return G
