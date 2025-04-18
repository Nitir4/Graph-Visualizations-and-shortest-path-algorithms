# ----------- SHORTEST PATH FUNCTIONS -----------

def find_shortest_path_dijkstra(G):
    """
    Runs Dijkstra's algorithm using NetworkX.
    """
    source = int(input("Enter the source node: "))
    target = int(input("Enter the target node: "))
    if nx.has_path(G, source, target):
        result, elapsed_time = measure_execution_time(nx.dijkstra_path, G, source, target, weight='weight')
        path_length = nx.dijkstra_path_length(G, source, target, weight='weight')
        print(f"Dijkstra's Shortest Path: {result}")
        print(f"Path Length: {path_length}")
        print(f"Execution Time: {elapsed_time:.6f} seconds")
    else:
        print(f"No path exists between node {source} and node {target}.")

def improved_dijkstra(G, source, target):
    """
    Custom implementation of Dijkstra's algorithm using a priority queue.
    """
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

def find_shortest_path_improved_dijkstra(G):
    """
    Wrapper for the improved Dijkstra's algorithm with timing.
    """
    source = int(input("Enter the source node: "))
    target = int(input("Enter the target node: "))
    if nx.has_path(G, source, target):
        result, elapsed_time = measure_execution_time(improved_dijkstra, G, source, target)
        path, length = result
        print(f"\nImproved Dijkstra's Shortest Path from node {source} to node {target}: {path}")
        print(f"Total path length: {length}")
        print(f"Execution time: {elapsed_time:.6f} seconds")
    else:
        print(f"No path exists between node {source} and node {target}.")

def find_shortest_path_bellman_ford(G):
    """
    Runs Bellman-Ford algorithm using NetworkX.
    """
    source = int(input("Enter the source node: "))
    target = int(input("Enter the target node: "))
    if nx.has_path(G, source, target):
        result, elapsed_time = measure_execution_time(nx.single_source_bellman_ford_path, G, source, weight='weight')
        path = result[target]
        path_length = nx.single_source_bellman_ford_path_length(G, source, weight='weight')[target]
        print(f"Bellman-Ford's Shortest Path: {path}")
        print(f"Path Length: {path_length}")
        print(f"Execution Time: {elapsed_time:.6f} seconds")
    else:
        print(f"No path exists between node {source} and node {target}.")

def find_shortest_path_floyd_warshall(G):
    """
    Runs Floyd-Warshall algorithm for all-pairs shortest paths.
    """
    result, elapsed_time = measure_execution_time(nx.floyd_warshall, G, weight='weight')
    print("\nFloyd-Warshall Shortest Paths:")
    for source, targets in result.items():
        for target, distance in targets.items():
            print(f"Shortest Path from {source} to {target}: {distance}")
    print(f"Execution Time: {elapsed_time:.6f} seconds")


