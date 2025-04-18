"""Compare the actual path algorithms, using one timing convention."""
import networkx as nx
from graph_core import timed_path, measure_execution_time


def compare_algorithms(graph):
    source = int(input('Enter the source node: '))
    target = int(input('Enter the target node: '))
    for algorithm in ['Dijkstra','Improved Dijkstra','Bellman-Ford','Floyd-Warshall']:
        try:
            path, length, seconds = timed_path(graph, source, target, algorithm)
            print(f'{algorithm}: Path={path}, Length={length}, Time={seconds:.6f}s')
        except (ValueError, nx.NetworkXException) as exc:
            print(f'{algorithm}: {exc}')
