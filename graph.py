import networkx as nx
from random import randint
from pyvis.network import Network



def create_graph():
    graph = nx.Graph()
    # graph_list =[[1,2],[1,4],[1,5],[5,4],[2,6],[7,6],[4,8],[8,9],[6,19],[19,10],
    #              [10,11],[10,7],[11,14],[11,17],[13,14],[13,7],[13,18],[18,8],[8,3],
    #              [3,12],[3,16],[16,15],[15,9],[14,17],[7,8],[3,9],[0,6],[0,8]]

    graph_list =[[1,2],[1,5],[1,7],[2,3],[2,9],[3,4],[3,11],[4,13],[4,5],[5,15],
                 [7,6],[7,8],[8,17],[8,9],[9,10],[10,18],[10,11],[12,19],[11,12],
                 [12,13],[14,0],[13,14],[14,15],[15,6],[6,16],[16,17],[17,18],
                 [18,19],[19,0],[0,16]]


    for el in graph_list:
        graph.add_edge(el[0], el[1], capacity=0)

    nx.draw(graph, with_labels = True)
    return graph

def graph_options(graph):
    graph.set_options("""
    var options = {
      "nodes": {
        "color": {
          "border": "rgba(97,233,74,1)",
          "background": "rgba(252,220,0,1)",
          "highlight": {
            "border": "rgba(233,15,0,1)",
            "background": "rgba(255,97,11,1)"
          },
          "hover": {
            "border": "rgba(225,233,52,1)"
          }
        },
        "shape": "circle"
      },
      "edges": {
        "color": {
          "inherit": true
        },
        "smooth": false
      },
      "physics": {
        "enabled": false,
        "minVelocity": 0.75
      }
    }
    """)

def draw_graph(networkx_graph, output_filename='graph.html', show_buttons=False):
    pyvis_graph = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="black")
    graph_options(pyvis_graph)

    for node, node_attrs in networkx_graph.nodes(data=True):
        pyvis_graph.add_node(node, **node_attrs)

    for source, target, edge_attrs in networkx_graph.edges(data=True):
        edge_attrs['label'] = edge_attrs['capacity']
        edge_attrs['value'] = edge_attrs['capacity']
        pyvis_graph.add_edge(source, target, **edge_attrs)
    if show_buttons:
        pyvis_graph.show_buttons()

    return pyvis_graph.show(output_filename)
