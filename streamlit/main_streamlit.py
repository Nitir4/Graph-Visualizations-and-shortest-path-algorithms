import streamlit as st
from graph_generator_streamlit import handle_random_graph
from shortest_paths_streamlit import find_shortest_path_improved_dijkstra
from comparison_streamlit import calculate_and_display

def main():
    st.title("Graph Generator and Shortest Path Finder")
    
    graph_choice = st.radio("Do you want a random or user-defined graph?", ["random", "exit"])

    if graph_choice == "random":
        G = handle_random_graph()
        st.subheader("Choose an Algorithm to Find the Shortest Path:")
        algo_choice = st.selectbox("Choose an algorithm", ["Improved Dijkstra's Algorithm"])

        if algo_choice == "Improved Dijkstra's Algorithm":
            find_shortest_path_improved_dijkstra(G)
    else:
        st.write("Exiting the application.")

if __name__ == "__main__":
    main()
