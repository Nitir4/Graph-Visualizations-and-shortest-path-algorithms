"""Interactive wrappers for the shared, validated algorithms."""
from graph_core import improved_dijkstra, measure_execution_time, timed_path, floyd_all


def _find(graph, algorithm):
    source = int(input('Enter the source node: '))
    target = int(input('Enter the target node: '))
    path, length, seconds = timed_path(graph, source, target, algorithm)
    if path is None:
        print(f'No path exists between node {source} and node {target}.')
    else:
        print(f'{algorithm}: Path={path}, Length={length}, Time={seconds:.6f}s')


def find_shortest_path_dijkstra(graph): _find(graph, 'Dijkstra')
def find_shortest_path_improved_dijkstra(graph): _find(graph, 'Improved Dijkstra')
def find_shortest_path_bellman_ford(graph): _find(graph, 'Bellman-Ford')


def find_shortest_path_floyd_warshall(graph):
    (paths, distances), seconds = measure_execution_time(floyd_all, graph)
    for source in graph:
        for target in graph:
            print(f'{source} → {target}: {distances[source][target]}')
    print(f'Execution Time: {seconds:.6f}s')
