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

def find_shortest_path_dijkstra(G, source, target):
    if nx.has_path(G, source, target):
        result, elapsed_time = measure_execution_time(nx.dijkstra_path, G, source, target, weight='weight')
        path_length = nx.dijkstra_path_length(G, source, target, weight='weight')
        return result, path_length, elapsed_time
    else:
        return None, None, None

def find_shortest_path_improved_dijkstra(G, source, target):
    if nx.has_path(G, source, target):
        result, elapsed_time = measure_execution_time(improved_dijkstra, G, source, target)
        path, length = result
        return path, length, elapsed_time
    else:
        return None, None, None

def find_shortest_path_bellman_ford(G, source, target):
    if nx.has_path(G, source, target):
        result, elapsed_time = measure_execution_time(nx.single_source_bellman_ford_path, G, source, weight='weight')
        path = result[target]
        path_length = nx.single_source_bellman_ford_path_length(G, source, weight='weight')[target]
        return path, path_length, elapsed_time
    else:
        return None, None, None

def find_shortest_path_floyd_warshall(G):
    result, elapsed_time = measure_execution_time(nx.floyd_warshall, G, weight='weight')
    return result, elapsed_time

# Compare all algorithms
def compare_all_algorithms(G, source, target):
    dijkstra_result, dijkstra_length, dijkstra_time = find_shortest_path_dijkstra(G, source, target)
    improved_dijkstra_result, improved_dijkstra_length, improved_dijkstra_time = find_shortest_path_improved_dijkstra(G, source, target)
    bellman_ford_result, bellman_ford_length, bellman_ford_time = find_shortest_path_bellman_ford(G, source, target)
    floyd_warshall_result, floyd_warshall_time = find_shortest_path_floyd_warshall(G)

    st.write(f"\n--- Dijkstra ---")
    if dijkstra_result:
        st.write(f"Path: {dijkstra_result}, Length: {dijkstra_length}, Time: {dijkstra_time:.6f}s")
    else:
        st.write("No path found")

    st.write(f"\n--- Improved Dijkstra ---")
    if improved_dijkstra_result:
        st.write(f"Path: {improved_dijkstra_result}, Length: {improved_dijkstra_length}, Time: {improved_dijkstra_time:.6f}s")
    else:
        st.write("No path found")

    st.write(f"\n--- Bellman-Ford ---")
    if bellman_ford_result:
        st.write(f"Path: {bellman_ford_result}, Length: {bellman_ford_length}, Time: {bellman_ford_time:.6f}s")
    else:
        st.write("No path found")

    st.write(f"\n--- Floyd-Warshall ---")
    if floyd_warshall_result:
        st.write(f"All Pairs Shortest Paths: {floyd_warshall_result}")
    st.write(f"Time: {floyd_warshall_time:.6f}s")

# Algorithm selection
def select_shortest_path_algorithm(G):
    st.write("--- Shortest Path Algorithm Menu ---")
    algorithm_choice = st.selectbox("Choose an algorithm", ["Dijkstra", "Improved Dijkstra", "Bellman-Ford", "Floyd-Warshall", "Compare All"])

    source = st.number_input("Enter the source node:", min_value=0)
    target = st.number_input("Enter the target node:", min_value=0)

    if algorithm_choice == "Dijkstra":
        find_shortest_path_dijkstra(G, source, target)
    elif algorithm_choice == "Improved Dijkstra":
        find_shortest_path_improved_dijkstra(G, source, target)
    elif algorithm_choice == "Bellman-Ford":
        find_shortest_path_bellman_ford(G, source, target)
    elif algorithm_choice == "Floyd-Warshall":
        find_shortest_path_floyd_warshall(G)
    elif algorithm_choice == "Compare All":
        compare_all_algorithms(G, source, target)

def main():
    # Initialize session state for graph if not already done
    if 'graph' not in st.session_state:
        st.session_state.graph = None

    st.write("--- Graph Generator and Shortest Path Finder ---")
    
    graph_choice = st.radio("Do you want a random or user-defined graph?", ("random", "user-defined"))

    # Only generate the graph if it doesn't exist already in session_state
    if graph_choice == "random" and st.session_state.graph is None:
        st.session_state.graph = handle_random_graph()
    elif graph_choice == "user-defined" and st.session_state.graph is None:
        st.session_state.graph = handle_user_defined_graph()

    # Always show the selected graph and its adjacency matrix if it exists
    if st.session_state.graph:
        st.write("--- Graph Display ---")
        draw_graph(st.session_state.graph)
        st.write("--- Adjacency Matrix ---")
        print_adjacency_matrix(st.session_state.graph)

    select_shortest_path_algorithm(st.session_state.graph)

if __name__ == "__main__":
    main()
