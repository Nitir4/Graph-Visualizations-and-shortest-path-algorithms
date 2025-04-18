import random
import networkx as nx
import matplotlib.pyplot as plt

from graph_core import generate_random_graph, graph_from_adjacency
from graph_drawing import graph_figure

def draw_graph(G):
    figure = graph_figure(G)
    plt.show()
    plt.close(figure)

def print_adjacency_matrix(G):
    adj_matrix = nx.adjacency_matrix(G).todense()
    print("Adjacency Matrix:")
    print(adj_matrix)

def handle_random_graph():
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
    directed = input("Should the graph be directed? (yes/no): ").strip().lower() == "yes"
    weighted = input("Should the graph be weighted? (yes/no): ").strip().lower() == "yes"
    num_nodes = int(input("Enter the number of nodes: "))

    print('Enter the square adjacency matrix row by row (space-separated values):')
    rows = [list(map(float, input(f'Row {i+1}: ').split())) for i in range(num_nodes)]
    G = graph_from_adjacency(rows, directed, weighted)

    print("\n--- Adjacency Matrix ---")
    print_adjacency_matrix(G)
    draw_graph(G)
    return G
