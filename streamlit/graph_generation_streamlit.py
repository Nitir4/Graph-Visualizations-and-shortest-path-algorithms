import networkx as nx
import random
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

def handle_random_graph(num_nodes, edge_prob, directed, weighted, min_weight=1, max_weight=10):
    G = generate_random_graph(num_nodes, edge_prob, directed, weighted, min_weight, max_weight)
    return G

def handle_user_defined_graph(num_nodes, adj_matrix, directed, weighted):
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j, weight in enumerate(adj_matrix[i]):
            if weight != 0:
                if weighted:
                    G.add_edge(i, j, weight=weight)
                else:
                    G.add_edge(i, j)
    return G

def display_graph_and_adjacency(G):
    import matplotlib.pyplot as plt
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    if nx.get_edge_attributes(G, 'weight'):
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    else:
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
    plt.show()

    adj_matrix = nx.adjacency_matrix(G).todense()
    return adj_matrix


