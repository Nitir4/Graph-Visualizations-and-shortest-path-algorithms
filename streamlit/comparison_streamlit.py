import streamlit as st
import networkx as nx
import heapq
import time
import math

# Timing utility
def measure_execution_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed_time = time.time() - start_time
    return result, elapsed_time

# Custom Dijkstra implementation
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

    return path

# Theoretical operation calculation
def calculate_theoretical_ops(V, E, algo_name):
    if algo_name in ["Dijkstra", "Improved Dijkstra"]:
        if V > 1:
            return (V + E) * math.log2(V)
    elif algo_name == "Bellman-Ford":
        return V * E
    elif algo_name == "Floyd-Warshall":
        return V ** 3
    return None

# Core comparison function
def compare_algorithms(G, source, target):
    st.subheader("⏱️ Time and Complexity Comparison")

    V = len(G.nodes())
    E = len(G.edges())

    edge_weights = nx.get_edge_attributes(G, 'weight')
    is_unweighted = len(edge_weights) == 0

    if is_unweighted:
        st.info("Graph is unweighted. Assigning default weight = 1 to all edges.")
        for u, v in G.edges():
            G[u][v]['weight'] = 1
    else:
        st.success("Graph is already weighted.")

    if not nx.has_path(G, source, target):
        st.error(f"No path exists between node {source} and node {target}.")
        return

    def display_result(algo_name, func, *args, **kwargs):
        st.markdown(f"### {algo_name}")
        theoretical_ops = calculate_theoretical_ops(V, E, algo_name.split()[0])
        try:
            result, elapsed_time = measure_execution_time(func, *args, **kwargs)
            st.write(f"Measured Time: `{elapsed_time:.6f}` seconds")
            if theoretical_ops:
                time_per_op = elapsed_time / theoretical_ops
                st.write(f"Theoretical Ops: `{theoretical_ops:.2f}`")
                st.write(f"Time per Operation: `{time_per_op:.10f}` seconds/op")
            else:
                st.write("Theoretical Ops: N/A")
            st.success("Result: Path found")
        except Exception as e:
            st.error(f"Execution failed: {e}")

    display_result("Dijkstra's Algorithm", nx.dijkstra_path, G, source, target, weight='weight')
    display_result("Improved Dijkstra's Algorithm", improved_dijkstra, G, source, target)
    display_result("Bellman-Ford Algorithm", nx.single_source_bellman_ford_path, G, source, weight='weight')
    display_result("Floyd-Warshall Algorithm", nx.floyd_warshall_predecessor_and_distance, G, weight='weight')

    if is_unweighted:
        for u, v in G.edges():
            del G[u][v]['weight']
