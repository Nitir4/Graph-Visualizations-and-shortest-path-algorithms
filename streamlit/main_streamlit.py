from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st

from graph_core import (generate_random_graph, graph_from_adjacency, timed_path,
                        improved_dijkstra, floyd_all, measure_execution_time)
from graph_drawing import graph_figure

measure = measure_execution_time


def safe_dijkstra(graph, source, target): return timed_path(graph, source, target, 'Dijkstra')
def safe_improved(graph, source, target): return timed_path(graph, source, target, 'Improved Dijkstra')
def safe_bellman(graph, source, target): return timed_path(graph, source, target, 'Bellman-Ford')
def safe_floyd_single(graph, source, target): return timed_path(graph, source, target, 'Floyd-Warshall')


def safe_floyd_all(graph):
    (paths, distances), seconds = measure(floyd_all, graph)
    return paths, distances, seconds


def main():
    st.set_page_config(page_title='Graph Explorer', layout='wide')
    st.title('Graph Explorer')
    st.caption('Build a graph, explore its communities, and compare shortest paths.')
    if 'G' not in st.session_state:
        st.session_state.G = None
    with st.sidebar:
        kind = st.radio('Graph input', ['Random', 'Adjacency matrix'])
        directed = st.checkbox('Directed')
        weighted = st.checkbox('Weighted')
        if kind == 'Random':
            n = st.number_input('Nodes', min_value=1, max_value=50, value=5)
            p = st.slider('Edge probability', 0.0, 1.0, 0.3)
            min_w = st.number_input('Min weight', min_value=1, value=1) if weighted else 1
            max_w = st.number_input('Max weight', min_value=1, value=10) if weighted else 1
            if st.button('Generate Graph'):
                try:
                    st.session_state.G = generate_random_graph(n,p,directed,weighted,min_w,max_w)
                except ValueError as exc:
                    st.error(str(exc))
        else:
            text = st.text_area('Adjacency matrix', help='One space-separated row per line. Undirected matrices must be symmetric.')
            if st.button('Load Graph'):
                try:
                    rows = [list(map(float,row.split())) for row in text.splitlines() if row.strip()]
                    st.session_state.G = graph_from_adjacency(rows,directed,weighted)
                except ValueError as exc:
                    st.error(str(exc))
        clustered = st.checkbox('Separate communities', value=True)
        st.caption('Colors indicate structural communities. Red edges highlight a selected route.')
    graph = st.session_state.G
    if graph is None:
        st.info('Generate or load a graph first.'); return
    algorithm = st.selectbox('Algorithm', ['Dijkstra','Improved Dijkstra','Bellman-Ford','Floyd-Warshall','Compare All'])
    source_column, target_column = st.columns(2)
    source = source_column.selectbox('Source', list(graph), index=0)
    target = target_column.selectbox('Target', list(graph), index=min(1,len(graph)-1))
    highlighted = None
    if st.button('Run'):
        if algorithm == 'Floyd-Warshall':
            try:
                _, distances, seconds = safe_floyd_all(graph)
                st.dataframe(pd.DataFrame(distances).T)
                route, length, _ = safe_floyd_single(graph,source,target)
                highlighted = route
                st.write(f'Selected route: {route}, distance: {length}. All-pairs time: {seconds:.6f}s')
            except (ValueError,nx.NetworkXException) as exc:
                st.error(str(exc))
        else:
            choices = ['Dijkstra','Improved Dijkstra','Bellman-Ford','Floyd-Warshall'] if algorithm=='Compare All' else [algorithm]
            results=[]
            for name in choices:
                try:
                    route, length, seconds = timed_path(graph,source,target,name)
                    results.append(dict(Algorithm=name,Path=route,Distance=length,Seconds=seconds,Status='Found' if route else 'No path'))
                    if route: highlighted = route
                except (ValueError,nx.NetworkXException) as exc:
                    results.append(dict(Algorithm=name,Path=None,Distance=None,Seconds=None,Status=str(exc)))
            st.dataframe(pd.DataFrame(results),hide_index=True)
    canvas, adjacency = st.columns([2,1])
    with canvas:
        figure = graph_figure(graph,highlighted,clustered)
        st.pyplot(figure)
        plt.close(figure)
    with adjacency:
        st.subheader('Adjacency matrix')
        st.dataframe(nx.to_pandas_adjacency(graph,weight='weight'))


if __name__=='__main__':
    main()
