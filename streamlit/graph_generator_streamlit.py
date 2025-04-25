import streamlit as st
import networkx as nx
import heapq
import time

# Utility function
def measure_execution_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time

# Dijkstra using NetworkX
def find_shortest_path_dijkstra(G, source, target):
    if nx.has_path(G, source, target):
        result, elapsed_time = measure_execution_time(nx.dijkstra_path, G, source, target, weight='weight')
        path_length = nx.dijkstra_path_length(G, source, target, weight='weight')
        st.success("Dijkstra's Algorithm Results:")
        st.write(f"Path: {result}")
        st.write(f"Path Length: {path_length}")
        st.write(f"Execution Time: {elapsed_time:.6f} seconds")
    else:
        st.error(f"No path exists between node {source} and node {target}.")

# Custom Dijkstra
def improved_dijkstra(G, source, target):
    pq = [(0, source)]
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

def find_shortest_path_improved_dijkstra(G, source, target):
    if nx.has_path(G, source, target):
        result, elapsed_time = measure_execution_time(improved_dijkstra, G, source, target)
        path, length = result
        st.success("Improved Dijkstra Results:")
        st.write(f"Path: {path}")
        st.write(f"Path Length: {length}")
        st.write(f"Execution Time: {elapsed_time:.6f} seconds")
    else:
        st.error(f"No path exists between node {source} and node {target}.")

# Bellman-Ford
def find_shortest_path_bellman_ford(G, source, target):
    if nx.has_path(G, source, target):
        result, elapsed_time = measure_execution_time(nx.single_source_bellman_ford_path, G, source, weight='weight')
        path = result[target]
        path_length = nx.single_source_bellman_ford_path_length(G, source, weight='weight')[target]
        st.success("Bellman-Ford Results:")
        st.write(f"Path: {path}")
        st.write(f"Path Length: {path_length}")
        st.write(f"Execution Time: {elapsed_time:.6f} seconds")
    else:
        st.error(f"No path exists between node {source} and node {target}.")

# Floyd-Warshall
def find_shortest_path_floyd_warshall(G):
    result, elapsed_time = measure_execution_time(nx.floyd_warshall, G, weight='weight')
    st.success("Floyd-Warshall All-Pairs Shortest Paths:")
    for source, targets in result.items():
        for target, distance in targets.items():
            st.write(f"From {source} to {target}: {distance}")
    st.write(f"Execution Time: {elapsed_time:.6f} seconds")
