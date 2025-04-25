import networkx as nx
import random
import streamlit as st

def generate_random_graph(num_nodes, edge_prob, directed, weighted, min_weight=1, max_weight=10):
    G = nx.DiGraph() if directed else nx.Graph()
    for i in range(num_nodes):
        G.add_node(i)
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and random.random() < edge_prob:
                if weighted:
                    weight = random.randint(min_weight, max_weight)
                    G.add_edge(i, j, weight=weight)
                else:
                    G.add_edge(i, j)
    return G

def handle_random_graph(num_nodes, edge_prob, directed, weighted, min_weight=1, max_weight=10):
    G = generate_random_graph(num_nodes, edge_prob, directed, weighted, min_weight, max_weight)
    return G

def handle_user_defined_graph(num_nodes, adj_matrix, directed, weighted):
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j, weight in enumerate(adj_matrix[i]):
            if weight != 0:
                if weighted:
                    G.add_edge(i, j, weight=weight)
                else:
                    G.add_edge(i, j)
    return G

def display_graph_and_adjacency(G):
    import matplotlib.pyplot as plt
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    if nx.get_edge_attributes(G, 'weight'):
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    else:
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
    plt.show()

    adj_matrix = nx.adjacency_matrix(G).todense()
    return adj_matrix

def plot_networkx_graph(G):
    import plotly.graph_objects as go
    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_y.append(y0)
        edge_y.append(y1)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none', mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            )
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Graph Visualization',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)
                    ))

    st.plotly_chart(fig)

# You can then call `plot_networkx_graph(G)` after graph generation

