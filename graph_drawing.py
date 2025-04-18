"""Stable community layout and readable rendering for both interfaces."""
import math
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def cluster_layout(graph):
    undirected = graph.to_undirected()
    groups = []
    for component in nx.connected_components(undirected):
        subgraph = undirected.subgraph(component)
        if len(component) < 3 or subgraph.number_of_edges() == 0:
            groups.append(set(component))
        else:
            # Community weights measure connection strength, not path costs.
            groups.extend(nx.community.greedy_modularity_communities(subgraph, weight=None))
    positions, colors = {}, {}
    groups.sort(key=lambda nodes: (str(min(nodes, key=str)), len(nodes)))
    count = len(groups)
    for index, nodes in enumerate(groups):
        radius = max(2.8, 1.2 * count)
        angle = 2 * math.pi * index / max(count, 1)
        center = np.array([radius*math.cos(angle), radius*math.sin(angle)]) if count > 1 else np.zeros(2)
        local = nx.spring_layout(undirected.subgraph(sorted(nodes, key=str)), seed=42, weight=None, scale=1)
        for node in nodes:
            positions[node] = local[node] + center
            colors[node] = index
    return positions, colors


def graph_figure(graph, path=None, clustered=True):
    figure, axis = plt.subplots(figsize=(10, 7), layout='constrained')
    figure.patch.set_facecolor('#f7f9fc')
    axis.set_facecolor('#f7f9fc')
    positions, groups = cluster_layout(graph)
    if not clustered:
        positions = nx.spring_layout(graph, seed=42, weight=None)
    nodes = list(graph)
    palette = plt.get_cmap('tab20')
    nx.draw_networkx_nodes(graph, positions, ax=axis, node_color=[palette(groups[n]%20) for n in nodes],
                           edgecolors='white', linewidths=1.8, node_size=650)
    nx.draw_networkx_labels(graph, positions, ax=axis, font_size=10, font_weight='bold')
    arrow_style = dict(arrows=True, arrowsize=18, connectionstyle='arc3,rad=0.09') if graph.is_directed() else {}
    nx.draw_networkx_edges(graph, positions, ax=axis, edge_color='#94a3b8', alpha=.65, width=1.4, **arrow_style)
    weighted_labels = {(u,v):f'{data["weight"]:g}' for u,v,data in graph.edges(data=True) if data.get('weight',1)!=1}
    if path and len(path)>1:
        nx.draw_networkx_edges(graph, positions, edgelist=list(zip(path,path[1:])), ax=axis,
                               edge_color='#e11d48', width=3, **arrow_style)
    if weighted_labels:
        nx.draw_networkx_edge_labels(graph, positions, weighted_labels, ax=axis, font_size=8,
                                     bbox=dict(facecolor='#f7f9fc',edgecolor='none',alpha=.85))
    axis.set_title(f'{len(graph)} nodes · {graph.number_of_edges()} edges',loc='left',fontsize=15,pad=18)
    axis.margins(.18)
    axis.axis('off')
    return figure
