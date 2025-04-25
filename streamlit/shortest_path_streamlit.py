import networkx as nx
import heapq
import streamlit as st


def dijkstra(G, source, target):
    return nx.dijkstra_path(G, source, target, weight='weight')

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

def bellman_ford(G, source, target):
    return nx.single_source_bellman_ford_path(G, source, weight='weight')[target]

def floyd_warshall(G):
    return nx.floyd_warshall(G, weight='weight')

def execute_shortest_path_algorithm(G, algo_choice, source, target):
    if algo_choice == "Dijkstra's Algorithm":
        return dijkstra(G, source, target)
    elif algo_choice == "Improved Dijkstra's Algorithm":
        return improved_dijkstra(G, source, target)
    elif algo_choice == "Bellman-Ford Algorithm":
        return bellman_ford(G, source, target)
    elif algo_choice == "Floyd-Warshall Algorithm":
        return floyd_warshall(G)
