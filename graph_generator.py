import random
import time
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import math

# ----------- GRAPH GENERATION & DISPLAY -----------

def generate_random_graph(num_nodes, edge_prob, directed, weighted, min_weight=1, max_weight=10):
    """
    Generates a random graph with the specified parameters.
    """
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
    """
    Draws the graph using matplotlib and NetworkX spring layout.
    """
    pos = nx.spring_layout(G)
    if nx.get_edge_attributes(G, 'weight'):
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    else:
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
    plt.show()

def print_adjacency_matrix(G):
    """
    Prints the adjacency matrix of the graph.
    """
    adj_matrix = nx.adjacency_matrix(G).todense()
    print("Adjacency Matrix:")
    print(adj_matrix)

# ----------- USER INPUT HANDLERS -----------

def handle_random_graph():
    """
    Prompts user for parameters and creates a random graph.
    """
    num_nodes = int(input("Enter the number of nodes: "))
    edge_prob = float(input("Enter the edge creation probability (0-1): "))
    directed = input("Should the graph be directed? (yes/no): ").strip().lower() == "yes"
    weighted = input("Should the graph be weighted? (yes/no): ").strip().lower() == "yes"

    if weighted:
        min_weight = int(input("Enter the minimum weight: "))
        max_weight = int(input("Enter the maximum weight: "))
        G = generate_random_graph(num_nodes, edge_prob, directed, weighted, min_weight, max_weight)
    else:
        G = generate_random_graph(num_nodes, edge_prob, directed, weighted)

    print("\n--- Adjacency Matrix ---")
    print_adjacency_matrix(G)
    draw_graph(G)
    return G

def handle_user_defined_graph():
    """
    Takes an adjacency matrix input from the user and creates a graph.
    """
    directed = input("Should the graph be directed? (yes/no): ").strip().lower() == "yes"
    weighted = input("Should the graph be weighted? (yes/no): ").strip().lower() == "yes"
    num_nodes = int(input("Enter the number of nodes: "))

    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(range(num_nodes))

    print("Enter the adjacency matrix row by row (space-separated values):")
    for i in range(num_nodes):
        row = list(map(float, input(f"Row {i + 1}: ").strip().split()))
        for j, weight in enumerate(row):
            if weight != 0:
                if weighted:
                    G.add_edge(i, j, weight=weight)
                else:
                    G.add_edge(i, j)

    print("\n--- Adjacency Matrix ---")
    print_adjacency_matrix(G)
    draw_graph(G)
    return G

