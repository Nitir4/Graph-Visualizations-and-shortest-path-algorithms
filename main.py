def select_shortest_path_algorithm(G):
    while True:
        print("\n--- Shortest Path Algorithm Menu ---")
        print("1. Dijkstra's Algorithm")
        print("2. Improved Dijkstra's Algorithm")
        print("3. Bellman-Ford Algorithm")
        print("4. Floyd-Warshall Algorithm (all pairs)")
        print("5. Compare All Algorithms (time and results)")
        print("6. Exit")

        choice = int(input("Enter your choice (1-6): "))
        if choice == 1:
            find_shortest_path_dijkstra(G)
        elif choice == 2:
            find_shortest_path_improved_dijkstra(G)
        elif choice == 3:
            find_shortest_path_bellman_ford(G)
        elif choice == 4:
            find_shortest_path_floyd_warshall(G)
        elif choice == 5:
            compare_algorithms(G)
        elif choice == 6:
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    print("--- Graph Generator and Shortest Path Finder ---")
    while True:
        graph_choice = input("Do you want a random or user-defined graph? (random/user-defined/exit): ").strip().lower()
        if graph_choice == "random":
            G = handle_random_graph()
            select_shortest_path_algorithm(G)
        elif graph_choice == "user-defined":
            G = handle_user_defined_graph()
            select_shortest_path_algorithm(G)
        elif graph_choice == "exit":
            break
        else:
            print("Invalid choice.")
