import time
import math
import streamlit as st

def measure_execution_time(func, *args, **kwargs):
    start_time = time.time()
    try:
        result = func(*args, **kwargs)
    except Exception as e:
        print(f"Error in function execution: {e}")
        return None, None  # Return None for both result and elapsed time in case of error
    
    elapsed_time = time.time() - start_time
    return result, elapsed_time


def calculate_theoretical_time(V, E, algo_name):
    if algo_name == "Dijkstra" or algo_name == "Improved Dijkstra":
        operations = (V + E) * math.log2(V)
        return f"Theoretical Operations: (V + E) log V ≈ ({V} + {E}) log2({V}) = {operations:.2f} operations"
    elif algo_name == "Bellman-Ford":
        operations = V * E
        return f"Theoretical Operations: V * E ≈ {V} * {E} = {operations:.2f} operations"
    elif algo_name == "Floyd-Warshall":
        operations = V**3
        return f"Theoretical Operations: V^3 ≈ {V}^3 = {operations:.2f} operations"
    else:
        return "Unknown Algorithm"

def compare_algorithms(G, algo_choice, source, target):
    print(f"Graph: {G}")
    print(f"Algorithm Choice: {algo_choice}")
    print(f"Source Node: {source}, Target Node: {target}")
    
    # Measure execution time and check result
    result, elapsed_time = measure_execution_time(execute_shortest_path_algorithm, G, algo_choice, source, target)
    
    # Debugging output
    print(f"Result: {result}")
    print(f"Elapsed Time: {elapsed_time}")
    
    # Check if the result or elapsed_time are None
    if result is None or elapsed_time is None:
        print("Error: result or elapsed_time is None")
        return None, None, None
    
    V = len(G.nodes())
    E = len(G.edges())
    theoretical_time = calculate_theoretical_time(V, E, algo_choice)
    return result, elapsed_time, theoretical_time


