import streamlit as st
from graph_generation import handle_random_graph, handle_user_defined_graph
from shortest_path_algorithms import find_shortest_path_dijkstra

def main():
    st.title("Graph Algorithm Visualizer")
    
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Graph Generation", "Shortest Path Algorithms"])

    if page == "Graph Generation":
        graph_choice = st.radio("Choose graph type", ("Random Graph", "User Defined Graph"))
        
        if graph_choice == "Random Graph":
            G = handle_random_graph()
        elif graph_choice == "User Defined Graph":
            G = handle_user_defined_graph()
    
    elif page == "Shortest Path Algorithms":
        G = handle_random_graph()  # Re-generate or use an existing graph from previous step
        st.subheader("Choose Shortest Path Algorithm")
        algo_choice = st.radio("Choose an algorithm", ("Dijkstra's Algorithm"))
        
        if algo_choice == "Dijkstra's Algorithm":
            find_shortest_path_dijkstra(G)

if __name__ == "__main__":
    main()
