import streamlit as st
from graph_generation_streamlit import handle_random_graph, handle_user_defined_graph, display_graph_and_adjacency
from shortest_path_streamlit import execute_shortest_path_algorithm
from comparison_streamlit import compare_algorithms

def main():
    st.title("Graph Generator and Shortest Path Finder")

    graph_choice = st.selectbox(
        "Choose Graph Type",
        ["Random Graph", "User Defined Graph"]
    )

    if graph_choice == "Random Graph":
        num_nodes = st.number_input("Enter the number of nodes:", min_value=1, max_value=100, value=5)
        edge_prob = st.slider("Enter the edge creation probability (0-1):", min_value=0.0, max_value=1.0, value=0.5)
        directed = st.radio("Should the graph be directed?", ('Yes', 'No')) == 'Yes'
        weighted = st.radio("Should the graph be weighted?", ('Yes', 'No')) == 'Yes'
        G = handle_random_graph(num_nodes, edge_prob, directed, weighted)
        adj_matrix = display_graph_and_adjacency(G)
        st.write("\n--- Adjacency Matrix ---")
        st.write(adj_matrix)

    elif graph_choice == "User Defined Graph":
        num_nodes = st.number_input("Enter the number of nodes:", min_value=1, max_value=100, value=5)
        adj_matrix = []
        for i in range(num_nodes):
            row_input = st.text_input(f"Row {i + 1}:")
            row = list(map(float, row_input.strip().split()))
            adj_matrix.append(row)
        directed = st.radio("Should the graph be directed?", ('Yes', 'No')) == 'Yes'
        weighted = st.radio("Should the graph be weighted?", ('Yes', 'No')) == 'Yes'
        G = handle_user_defined_graph(num_nodes, adj_matrix, directed, weighted)
        adj_matrix = display_graph_and_adjacency(G)
        st.write("\n--- Adjacency Matrix ---")
        st.write(adj_matrix)

    st.write("\n--- Shortest Path Algorithm ---")
    algo_choice = st.selectbox(
        "Select Shortest Path Algorithm",
        ["Dijkstra's Algorithm", "Improved Dijkstra's Algorithm", "Bellman-Ford Algorithm", "Floyd-Warshall Algorithm"]
    )
    source = st.number_input("Enter the source node:", min_value=0, value=0)
    target = st.number_input("Enter the target node:", min_value=0, value=1)

    result, elapsed_time, theoretical_time = compare_algorithms(G, algo_choice, source, target)

    st.write(f"Result: {result}")
    st.write(f"Execution Time: {elapsed_time:.6f} seconds")
    st.write(f"Theoretical Time Complexity: {theoretical_time}")

if __name__ == "__main__":
    main()
