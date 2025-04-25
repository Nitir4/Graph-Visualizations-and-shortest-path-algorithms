import random
import time
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import math
import streamlit as st

# Graph generation functions
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
    st.pyplot(plt)

def print_adjacency_matrix(G):
    adj_matrix = nx.adjacency_matrix(G).todense()
    st.write("Adjacency Matrix:")
    st.write(adj_matrix)

def handle_random_graph():
    num_nodes = st.number_input("Enter the number of nodes:", min_value=1, value=5)
    edge_prob = st.slider("Enter the edge creation probability (0-1):", 0.0, 1.0, 0.3)
    directed = st.radio("Should the graph be directed?", ("Yes", "No")) == "Yes"
    weighted = st.radio("Should the graph be weighted?", ("Yes", "No")) == "Yes"

    if weighted:
        min_weight = st.number_input("Enter the minimum weight:", min_value=1, value=1)
        max_weight = st.number_input("Enter the maximum weight:", min_value=1, value=10)
        G = generate_random_graph(num_nodes, edge_prob, directed, weighted, min_weight, max_weight)
    else:
        G = generate_random_graph(num_nodes, edge_prob, directed, weighted)

    st.write("--- Adjacency Matrix ---")
    print_adjacency_matrix(G)
    draw_graph(G)
    return G

def handle_user_defined_graph():
    directed = st.radio("Should the graph be directed?", ("Yes", "No")) == "Yes"
    weighted = st.radio("Should the graph be weighted?", ("Yes", "No")) == "Yes"
    num_nodes = st.number_input("Enter the number of nodes:", min_value=1, value=5)

    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(range(num_nodes))

    st.write("Enter the adjacency matrix row by row (space-separated values):")
    for i in range(num_nodes):
        row = st.text_input(f"Row {i+1}:")
        row_values = list(map(float, row.strip().split()))
        for j, weight in enumerate(row_values):
            if weight != 0:
                if weighted:
                    G.add_edge(i, j, weight=weight)
                else:
                    G.add_edge(i, j)

    st.write("--- Adjacency Matrix ---")
    print_adjacency_matrix(G)
    draw_graph(G)
    return G

# Shortest path algorithms
def measure_execution_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed_time = time.time() - start_time
    return result, elapsed_time

def improved_dijkstra(G, source, target):
    pq = []
    heapq.heappush(pq, (0, source))

    distances = {node: float('inf') for node in G.nodes()}
    distances[source] = 0
    predecessors = {node: None for node in G.nodes()}

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node == target:
            break
        for neighbor, attributes in G[current_node].items():
            weight = attributes.get('weight', 1)
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    path = []
    current = target
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()

    return path, distances[target]

def find_shortest_path_dijkstra(G):
    source = st.number_input("Enter the source node:", min_value=0)
    target = st.number_input("Enter the target node:", min_value=0)
    if nx.has_path(G, source, target):
        result, elapsed_time = measure_execution_time(nx.dijkstra_path, G, source, target, weight='weight')
        path_length = nx.dijkstra_path_length(G, source, target, weight='weight')
        st.write(f"Dijkstra's Shortest Path: {result}")
        st.write(f"Path Length: {path_length}")
        st.write(f"Execution Time: {elapsed_time:.6f} seconds")
    else:
        st.write(f"No path exists between node {source} and node {target}.")

def find_shortest_path_improved_dijkstra(G):
    source = st.number_input("Enter the source node:", min_value=0)
    target = st.number_input("Enter the target node:", min_value=0)

    if nx.has_path(G, source, target):
        result, elapsed_time = measure_execution_time(improved_dijkstra, G, source, target)
        path, length = result
        st.write(f"\nImproved Dijkstra's Shortest Path: {path}")
        st.write(f"Total path length: {length}")
        st.write(f"Execution time: {elapsed_time:.6f} seconds")
    else:
        st.write(f"No path exists between node {source} and node {target}.")

def find_shortest_path_bellman_ford(G):
    source = st.number_input("Enter the source node:", min_value=0)
    target = st.number_input("Enter the target node:", min_value=0)
    if nx.has_path(G, source, target):
        result, elapsed_time = measure_execution_time(nx.single_source_bellman_ford_path, G, source, weight='weight')
        path = result[target]
        path_length = nx.single_source_bellman_ford_path_length(G, source, weight='weight')[target]
        st.write(f"Bellman-Ford's Shortest Path: {path}")
        st.write(f"Path Length: {path_length}")
        st.write(f"Execution Time: {elapsed_time:.6f} seconds")
    else:
        st.write(f"No path exists between node {source} and node {target}.")

def find_shortest_path_floyd_warshall(G):
    result, elapsed_time = measure_execution_time(nx.floyd_warshall, G, weight='weight')
    st.write("\nFloyd-Warshall Shortest Paths:")
    for source, targets in result.items():
        for target, distance in targets.items():
            st.write(f"Shortest Path from {source} to {target}: {distance}")
    st.write(f"Execution Time: {elapsed_time:.6f} seconds")

# Algorithm selection
def select_shortest_path_algorithm(G):
    st.write("--- Shortest Path Algorithm Menu ---")
    option = st.selectbox("Choose an algorithm:", [
        "Dijkstra's Algorithm",
        "Improved Dijkstra's Algorithm",
        "Bellman-Ford Algorithm",
        "Floyd-Warshall Algorithm (all pairs)"
    ])
    
    if option == "Dijkstra's Algorithm":
        find_shortest_path_dijkstra(G)
    elif option == "Improved Dijkstra's Algorithm":
        find_shortest_path_improved_dijkstra(G)
    elif option == "Bellman-Ford Algorithm":
        find_shortest_path_bellman_ford(G)
    elif option == "Floyd-Warshall Algorithm (all pairs)":
        find_shortest_path_floyd_warshall(G)

def main():
    st.title("Graph Generator and Shortest Path Finder")
    graph_choice = st.selectbox("Do you want a random or user-defined graph?", ["Random", "User-defined", "Exit"])

    if graph_choice == "Random":
        G = handle_random_graph()
        select_shortest_path_algorithm(G)
    elif graph_choice == "User-defined":
        G = handle_user_defined_graph()
        select_shortest_path_algorithm(G)
    else:
        st.write("Goodbye!")

if __name__ == "__main__":
    main()
