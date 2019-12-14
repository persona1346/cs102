from api import get_friends
import time
import igraph
from igraph import Graph, plot
import numpy as np

def get_network(users_ids, as_edgelist=True):
    edges=[]

    if as_edgelist == False:
        for i in range(len(users_ids)):
            edges += [[]]
            for j in range(len(users_ids)):
                edges[i] += [0]

    for i in range(len(users_ids)):
        try:
            friends =  get_friends(users_ids[i],'')["response"]["items"]

            for j in range(len(users_ids)):
                if i != j and users_ids[j] in friends:
                    if as_edgelist:
                        edges += [(i,j)]
                    else:
                        edges[i][j] = 1

            time.sleep(0.3)
        except:
            pass


    # Создание графа
    g = Graph(vertex_attrs={"label":users_ids},
        edges=edges, directed=False)

    # Задаем стиль отображения графа
    N = len(users_ids)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**3,
        repulserad=N**3)

    g.simplify(multiple=True, loops=True)

    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    # Отрисовываем граф
    plot(g, **visual_style)



    pass
