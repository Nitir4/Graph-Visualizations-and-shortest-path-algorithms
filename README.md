# Graph-Visualizations-and-shortest-path-algorithms
This is something i worked on as a freshmen for my discrete mathematics final project. This is entirely based on graph theory.
It give two choices for the graphs be it user generated or random.
Furthermore for random graphs it asks you if you want the graph to be weighted, whether it should be a directed graph, and the edge creation possibility.
For user-defined graph it asks you to input the adjacency matrix.
It then generates the graph and then there are different modes of shortest path algorithms that can be applied on it

Install `requirements.txt`, then run `python main.py` for the CLI or
`streamlit run streamlit/main_streamlit.py` for the visual explorer.

Both interfaces use the same validated algorithms and graph construction.
Undirected random graphs sample each node pair once. Adjacency matrices must be
square and finite, and symmetric for undirected graphs. An unweighted nonzero
entry represents an edge of weight one. A zero entry represents no edge.

Disconnected routes report “No path.” Dijkstra rejects negative weights;
Bellman-Ford and Floyd-Warshall support them and report negative cycles instead
of an undefined route. The Floyd path reconstruction uses Floyd predecessors,
so it does not silently substitute Dijkstra on negative-weight graphs.

The visual explorer has stable community colors, separated clusters, directed
arrows, and highlighted routes. Community detection uses graph structure rather
than treating shortest-path costs as connection strengths.

Regression checks: `python -m pytest tests -q` (install `pytest` separately).
