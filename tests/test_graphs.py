import io
import math
import random
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pytest

from graph_core import generate_random_graph, graph_from_adjacency, shortest_path, timed_path, floyd_all
from graph_drawing import cluster_layout, graph_figure

ALGORITHMS=['Dijkstra','Improved Dijkstra','Bellman-Ford','Floyd-Warshall']


@pytest.mark.parametrize('algorithm',ALGORITHMS)
def test_disconnected_and_singleton_routes(algorithm):
    graph=nx.Graph(); graph.add_nodes_from([0,1])
    path,length,seconds=timed_path(graph,0,1,algorithm)
    assert path is length is None and seconds>=0
    assert shortest_path(graph,0,0,algorithm)==([0],0)
    with pytest.raises(nx.NodeNotFound): shortest_path(graph,0,8,algorithm)


@pytest.mark.parametrize('directed',[True,False])
@pytest.mark.parametrize('algorithm',ALGORITHMS)
def test_seeded_weighted_paths_agree_with_reference(directed,algorithm):
    random.seed(505)
    graph=generate_random_graph(12,.4,directed,True,1,10)
    for source in graph:
        for target in graph:
            expected=nx.shortest_path_length(graph,source,target,weight='weight')
            path,length=shortest_path(graph,source,target,algorithm)
            assert path[0]==source and path[-1]==target and length==expected
            assert sum(graph[u][v]['weight'] for u,v in zip(path,path[1:]))==length


def test_undirected_pairs_sampled_once(monkeypatch):
    calls=[]
    monkeypatch.setattr(random,'random',lambda: calls.append(1) or .4)
    graph=generate_random_graph(5,.5)
    assert len(calls)==10 and graph.number_of_edges()==10
    calls.clear()
    graph=generate_random_graph(5,.5,True)
    assert len(calls)==20 and graph.number_of_edges()==20


@pytest.mark.parametrize('rows',[[],[[0,1]],[[0,1],[0]],[[0,float('nan')],[1,0]],[[0,1],[0,0]]])
def test_invalid_undirected_adjacency_rejected(rows):
    with pytest.raises(ValueError): graph_from_adjacency(rows)


def test_directed_negative_edges_use_bellman_and_floyd_paths():
    graph=graph_from_adjacency([[0,2,4],[0,0,-3],[0,0,0]],True,True)
    for algorithm in ['Bellman-Ford','Floyd-Warshall']:
        assert shortest_path(graph,0,2,algorithm)==([0,1,2],-1)
    for algorithm in ['Dijkstra','Improved Dijkstra']:
        with pytest.raises(ValueError):shortest_path(graph,0,2,algorithm)
    graph.add_edge(2,1,weight=1)
    for algorithm in ['Bellman-Ford','Floyd-Warshall']:
        with pytest.raises(nx.NetworkXUnbounded):shortest_path(graph,0,2,algorithm)


def test_layout_is_repeatable_and_includes_isolated_nodes():
    graph=nx.disjoint_union(nx.complete_graph(5),nx.complete_graph(4))
    graph.add_edge(4,5);graph.add_node(9)
    first, colors=cluster_layout(graph)
    second,_=cluster_layout(graph)
    assert set(first)==set(graph)==set(colors)
    for node in graph: np.testing.assert_allclose(first[node],second[node])
    assert all(np.isfinite(pos).all() for pos in first.values())
    figure=graph_figure(graph,[0,4,5,8])
    buffer=io.BytesIO();figure.savefig(buffer,format='png');plt.close(figure)
    assert buffer.getbuffer().nbytes>1000


def test_cli_entrypoint_and_comparison_are_wired(monkeypatch,capsys):
    import main
    from comparison import compare_algorithms
    answers=iter(['exit'])
    monkeypatch.setattr('builtins.input',lambda *args:next(answers))
    main.main()
    answers=iter(['0','1'])
    compare_algorithms(nx.path_graph(2))
    assert 'Floyd-Warshall' in capsys.readouterr().out


def test_streamlit_singleton_and_disconnected_compare():
    from streamlit.testing.v1 import AppTest
    app=AppTest.from_file(Path(__file__).resolve().parents[1]/'streamlit/main_streamlit.py').run(timeout=20)
    def click(label):
        next(button for button in app.button if button.label==label).click().run(timeout=20)
    app.number_input[0].set_value(1)
    click('Generate Graph')
    assert not app.exception
    assert app.selectbox[2].value==0
    app.selectbox[0].select('Compare All')
    click('Run')
    assert not app.exception
    app.number_input[0].set_value(2)
    app.slider[0].set_value(0.)
    click('Generate Graph')
    app.selectbox[2].select(1)
    click('Run')
    assert not app.exception
    assert set(app.dataframe[0].value['Status'])=={'No path'}
