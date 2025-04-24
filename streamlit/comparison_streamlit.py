import math
import networkx as nx
import streamlit as st
from shortest_paths_streamlit import measure_execution_time

def calculate_theoretical_time(V, E, algo_name):
    if algo_name == "Dijkstra" or algo_name == "Improved Dijkstra":
        operations = (V + E) * math.log2(V)
        return f"Theoretical Operations: (V + E) log V ≈ ({V} + {E}) log2({V}) = {operations:.2f} operations"
    elif algo_name == "Bellman-Ford":
        operations = V * E
        return f"Theoretical Operations: V * E ≈ {V} * {E} = {operations:.2f} operations"
    elif algo_name == "Floyd-Warshall":
        operations = V ** 3
        return f"Theoretical Operations: V^3 ≈ {V}^3 = {operations:.2f} operations"
    else:
        return "Unknown Algorithm"

def calculate_and_display(G, algo_name, func, *args, **kwargs):
    try:
        V = len(G.nodes())
        E = len(G.edges())

        theoretical_ops = calculate_theoretical_time(V, E, algo_name)
        st.write(theoretical_ops)

        result, elapsed_time = measure_execution_time(func, *args, **kwargs)

        time_per_op = elapsed_time / (V * E) if theoretical_ops != "Unknown Algorithm" else 0
        st.write(f"Measured Time: {elapsed_time:.6f} seconds")
        st.write(f"Time per Operation: {time_per_op:.10f} seconds/operation")

        return result
    except Exception as e:
        st.write(f"{algo_name} failed: {e}")
        return None
