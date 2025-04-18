def measure_execution_time(func, *args, **kwargs):
    """
    Measures execution time of a function call.
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed_time = time.time() - start_time
    return result, elapsed_time

def calculate_theoretical_time(V, E, algo_name):
    """
    Estimates theoretical number of operations for various algorithms.
    """
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


def calculate_and_display(G, algo_name, func, *args, **kwargs):
    """
    Calculates and displays time complexity, actual execution time, and time per operation.
    """
    try:
        print(f"\n[{algo_name}]")
        V = len(G.nodes())
        E = len(G.edges())

        # Estimate theoretical operations
        theoretical_ops = 0
        if algo_name in ["Dijkstra's Algorithm", "Improved Dijkstra's Algorithm"]:
            if V > 1:
                theoretical_ops = (V + E) * math.log2(V)
                print(f"Theoretical Operations: (V + E) log V ≈ ({V} + {E}) log2({V}) = {theoretical_ops:.2f}")
            else:
                print("Graph must have more than one vertex for Dijkstra's algorithm.")
        elif algo_name == "Bellman-Ford Algorithm":
            theoretical_ops = V * E
            print(f"Theoretical Operations: V * E ≈ {V} * {E} = {theoretical_ops:.2f}")
        elif algo_name == "Floyd-Warshall Algorithm":
            theoretical_ops = V ** 3
            print(f"Theoretical Operations: V^3 ≈ {V}^3 = {theoretical_ops:.2f}")

        result, elapsed_time = measure_execution_time(func, *args, **kwargs)

        if theoretical_ops > 0:
            time_per_op = elapsed_time / theoretical_ops
            print(f"Measured Time: {elapsed_time:.6f} seconds")
            print(f"Time per Operation: {time_per_op:.10f} seconds/operation")
        else:
            print(f"Measured Time: {elapsed_time:.6f} seconds")
            print(f"Time per Operation: N/A")

        return result
    except Exception as e:
        print(f"{algo_name} failed: {e}")
        return None

def compare_algorithms(G):
    """
    Compares all shortest path algorithms and shows timing and theoretical analysis.
    """
    V = len(G.nodes())
    E = len(G.edges())

    edge_weights = nx.get_edge_attributes(G, 'weight')
    is_unweighted = len(edge_weights) == 0

    if is_unweighted:
        print("Graph is unweighted. Assigning default weight = 1 to all edges.\n")
        for u, v in G.edges():
            G[u][v]['weight'] = 1
    else:
        print("Graph is already weighted.\n")

    source = int(input("Enter the source node: "))
    target = int(input("Enter the target node: "))
    if not nx.has_path(G, source, target):
        print(f"No path exists between node {source} and node {target}.")
        return

    print("\n--- Time, Operations, and Time-per-Operation Comparison ---\n")

    calculate_and_display(G, "Dijkstra's Algorithm", nx.dijkstra_path, G, source, target, weight='weight')
    calculate_and_display(G, "Improved Dijkstra's Algorithm", improved_dijkstra, G, source, target)
    calculate_and_display(G, "Bellman-Ford Algorithm", nx.single_source_bellman_ford_path, G, source, weight='weight')
    calculate_and_display(G, "Floyd-Warshall Algorithm", nx.floyd_warshall_predecessor_and_distance, G, weight='weight')

    if is_unweighted:
        for u, v in G.edges():
            del G[u][v]['weight']


