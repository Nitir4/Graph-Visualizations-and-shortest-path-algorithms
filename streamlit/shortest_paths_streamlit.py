import networkx as nx
import heapq
import time
import streamlit as st

def measure_execution_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed_time = time.time() - start_time
    return result, elapsed_time

def dijkstra(G, source, target):
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
    source = st.number_input("Enter the source node", min_value=0, value=0)
    target = st.number_input("Enter the target node", min_value=0, value=G.number_of_nodes() - 1)
    
    if nx.has_path(G, source, target):
        result, elapsed_time = measure_execution_time(dijkstra, G, source, target)
        path, length = result
        st.write(f"Shortest Path from node {source} to node {target}: {path}")
        st.write(f"Total path length: {length}")
        st.write(f"Execution time: {elapsed_time:.6f} seconds")
    else:
        st.error(f"No path exists between node {source} and node {target}.")
