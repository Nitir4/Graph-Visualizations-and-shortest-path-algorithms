"""Graph construction and shortest paths shared by CLI and Streamlit."""
import heapq
import itertools
import math
import numbers
import random
import time

import networkx as nx
import numpy as np


def measure_execution_time(function, *args, **kwargs):
    start = time.perf_counter()
    result = function(*args, **kwargs)
    return result, time.perf_counter() - start


def generate_random_graph(n, p, directed=False, weighted=False, min_weight=1, max_weight=10):
    if isinstance(n, bool) or not isinstance(n, numbers.Integral) or n < 1:
        raise ValueError('Choose at least one node.')
    if not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError('Edge probability must lie between 0 and 1.')
    if weighted and (min_weight < 1 or max_weight < min_weight):
        raise ValueError('Weights must satisfy 1 <= minimum <= maximum.')
    graph = nx.DiGraph() if directed else nx.Graph()
    graph.add_nodes_from(range(n))
    pairs = itertools.permutations(range(n), 2) if directed else itertools.combinations(range(n), 2)
    for source, target in pairs:
        if random.random() < p:
            graph.add_edge(source, target, weight=random.randint(min_weight, max_weight) if weighted else 1)
    return graph


def graph_from_adjacency(rows, directed=False, weighted=False):
    try:
        matrix = np.asarray(rows, dtype=float)
    except (ValueError, TypeError) as exc:
        raise ValueError('Enter a square numeric adjacency matrix.') from exc
    if matrix.ndim != 2 or len(matrix) < 1 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError('Enter a nonempty square adjacency matrix.')
    if not np.isfinite(matrix).all():
        raise ValueError('Adjacency entries must be finite.')
    values = matrix if weighted else (matrix != 0).astype(float)
    if not directed and not np.array_equal(values, values.T):
        raise ValueError('An undirected adjacency matrix must be symmetric.')
    return nx.from_numpy_array(values, create_using=nx.DiGraph if directed else nx.Graph)


def _nodes(graph, source, target):
    if source not in graph or target not in graph:
        raise nx.NodeNotFound('Source and target must be nodes in the graph.')


def _nonnegative(graph):
    if any(data.get('weight', 1) < 0 for _, _, data in graph.edges(data=True)):
        raise ValueError('Dijkstra requires nonnegative weights. Choose Bellman-Ford or Floyd-Warshall.')


def improved_dijkstra(graph, source, target):
    _nodes(graph, source, target)
    _nonnegative(graph)
    sequence = itertools.count()
    queue = [(0, next(sequence), source)]
    distances = {source: 0}
    previous = {}
    while queue:
        distance, _, node = heapq.heappop(queue)
        if distance != distances[node]:
            continue
        if node == target:
            path = [target]
            while path[-1] != source:
                path.append(previous[path[-1]])
            return path[::-1], distance
        for neighbor, attributes in graph[node].items():
            candidate = distance + attributes.get('weight', 1)
            if candidate < distances.get(neighbor, float('inf')):
                distances[neighbor] = candidate
                previous[neighbor] = node
                heapq.heappush(queue, (candidate, next(sequence), neighbor))
    raise nx.NetworkXNoPath(f'No path from {source} to {target}.')


def floyd_all(graph):
    predecessors, distances = nx.floyd_warshall_predecessor_and_distance(graph, weight='weight')
    if any(distances[node][node] < 0 for node in graph):
        raise nx.NetworkXUnbounded('A negative cycle makes shortest paths undefined.')
    paths = {}
    for source in graph:
        paths[source] = {}
        for target in graph:
            if math.isfinite(distances[source][target]):
                paths[source][target] = [source] if source == target else nx.reconstruct_path(source, target, predecessors)
    return paths, distances


def shortest_path(graph, source, target, algorithm):
    _nodes(graph, source, target)
    if algorithm == 'Dijkstra':
        _nonnegative(graph)
        length, path = nx.single_source_dijkstra(graph, source, target, weight='weight')
        return path, length
    if algorithm == 'Improved Dijkstra':
        return improved_dijkstra(graph, source, target)
    if algorithm == 'Bellman-Ford':
        distances, paths = nx.single_source_bellman_ford(graph, source, weight='weight')
        if target not in paths:
            raise nx.NetworkXNoPath(f'No path from {source} to {target}.')
        return paths[target], distances[target]
    if algorithm == 'Floyd-Warshall':
        paths, distances = floyd_all(graph)
        if target not in paths[source]:
            raise nx.NetworkXNoPath(f'No path from {source} to {target}.')
        return paths[source][target], distances[source][target]
    raise ValueError('Unknown shortest-path algorithm.')


def timed_path(graph, source, target, algorithm):
    start = time.perf_counter()
    try:
        path, length = shortest_path(graph, source, target, algorithm)
    except nx.NetworkXNoPath:
        return None, None, time.perf_counter()-start
    return path, length, time.perf_counter()-start
