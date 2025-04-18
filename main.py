import networkx as nx
from graph_generator import handle_random_graph, handle_user_defined_graph
from shortest_path import (find_shortest_path_dijkstra, find_shortest_path_improved_dijkstra,
                           find_shortest_path_bellman_ford, find_shortest_path_floyd_warshall)
from comparison import compare_algorithms

def select_shortest_path_algorithm(G):
    while True:
        print("\n--- Shortest Path Algorithm Menu ---")
        print("1. Dijkstra's Algorithm")
        print("2. Improved Dijkstra's Algorithm")
        print("3. Bellman-Ford Algorithm")
        print("4. Floyd-Warshall Algorithm (all pairs)")
        print("5. Compare All Algorithms (time and results)")
        print("6. Exit")

        try:
            choice = int(input('Enter your choice (1-6): '))
            if choice == 6:
                return
            functions = {1:find_shortest_path_dijkstra, 2:find_shortest_path_improved_dijkstra,
                         3:find_shortest_path_bellman_ford, 4:find_shortest_path_floyd_warshall,
                         5:compare_algorithms}
            if choice not in functions:
                print('Invalid choice.'); continue
            functions[choice](G)
        except (ValueError, nx.NetworkXException) as exc:
            print(f'Cannot run that selection: {exc}')

def main():
    print("--- Graph Generator and Shortest Path Finder ---")
    while True:
        graph_choice = input("Do you want a random or user-defined graph? (random/user-defined/exit): ").strip().lower()
        try:
            if graph_choice == 'random':
                select_shortest_path_algorithm(handle_random_graph())
            elif graph_choice == 'user-defined':
                select_shortest_path_algorithm(handle_user_defined_graph())
            elif graph_choice == 'exit':
                break
            else:
                print('Invalid choice.')
        except (ValueError, nx.NetworkXException) as exc:
            print(f'Cannot load graph: {exc}')

if __name__ == '__main__':
    main()
