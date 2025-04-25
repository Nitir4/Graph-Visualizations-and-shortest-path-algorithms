import streamlit as st
import time
import math
import networkx as nx

def measure_execution_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed_time = time.time() - start_time
    return result, elapsed_time

def calculate_theoretical_time(V, E, algo_name):
    if algo_name in ["Dijkstra's Algorithm", "Improved Dijkstra's Algorithm"]:
        operations = (V + E) * math.log2(V)
        return operations, f"(V + E) log V ≈ ({V} + {E}) log2({V}) = {operations:.2f} operations"
    elif algo_name == "Bellman-Ford Algorithm":
        operations = V * E
        return operations, f"V * E ≈ {V} * {E} = {operations:.2f} operations"
    elif algo_name == "Floyd-Warshall Algorithm":
        operations = V ** 3
        return operations, f"V^3 ≈ {V}^3 = {operations:.2f} operations"
    else:
        return 0, "Unknown Algorithm"

def calculate_and_display(G, algo_name, func, *args, **kwargs):
    V = len(G.nodes())
    E = len(G.edges())

    st.markdown(f"### {algo_name}")

    theoretical_ops, theory_str = calculate_theoretical_time(V, E, algo_name)
    st.write(f"**Theoretical Operations:** {theory_str}")

    try:
        result, elapsed_time = measure_execution_time(func, *args, **kwargs)
        if theoretical_ops > 0:
            time_per_op = elapsed_time / theoretical_ops
            st.write(f"**Measured Time:** {elapsed_time:.6f} seconds")
            st.write(f"**Time per Operation:** {time_per_op:.10f} seconds/operation")
        else:
            st.write(f"**Measured Time:** {elapsed_time:.6f} seconds")
            st.write("**Time per Operation:** N/A")
        return result
    except Exception as e:
        st.error(f"{algo_name} failed: {e}")
        return None

def compare_algorithms_streamlit(G, improved_dijkstra):
    if G is None:
        st.warning("Please generate or input a graph first.")
        return

    V = len(G.nodes())
    E = len(G.edges())

    edge_weights = nx.get_edge_attributes(G, 'weight')
    is_unweighted = len(edge_weights) == 0

    if is_unweighted:
        st.info("Graph is unweighted. Default weight = 1 assigned to all edges.")
        for u, v in G.edges():
            G[u][v]['weight'] = 1

    source = st.number_input("Enter source node", min_value=0, max_value=V-1, value=0)
    target = st.number_input("Enter target node", min_value=0, max_value=V-1, value=V-1)

    if st.button("Compare Algorithms"):
        if not nx.has_path(G, source, target):
            st.error(f"No path exists between node {source} and node {target}.")
            return

        st.subheader("⏱️ Time & Complexity Comparison")
        calculate_and_display(G, "Dijkstra's Algorithm", nx.dijkstra_path, G, source, target, weight='weight')
        calculate_and_display(G, "Improved Dijkstra's Algorithm", improved_dijkstra, G, source, target)
        calculate_and_display(G, "Bellman-Ford Algorithm", nx.single_source_bellman_ford_path, G, source, weight='weight')
        calculate_and_display(G, "Floyd-Warshall Algorithm", nx.floyd_warshall_predecessor_and_distance, G, weight='weight')

        if is_unweighted:
            for u, v in G.edges():
                del G[u][v]['weight']
