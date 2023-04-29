import networkx as nx
import random
from random import randint
import matplotlib.pyplot as plt


# Rucno kreirani klasterabilan graf
def klasterabilanGraf():
    graf = nx.Graph()
    for i in range(1, 19):
        graf.add_node(i)
    graf.add_edge(1, 2, sign="+")
    graf.add_edge(1, 3, sign="+")
    graf.add_edge(2, 3, sign="+")

    graf.add_edge(4, 5, sign="+")
    graf.add_edge(3, 4, sign="-")

    graf.add_edge(2, 6, sign="-")
    graf.add_edge(6, 7, sign="-")
    graf.add_edge(7, 8, sign="-")
    graf.add_edge(8, 9, sign="-")

    graf.add_edge(9, 10, sign="+")
    graf.add_edge(9, 11, sign="+")
    graf.add_edge(10, 11, sign="+")
    graf.add_edge(11, 12, sign="+")
    graf.add_edge(11, 14, sign="-")

    graf.add_edge(15, 13, sign="-")
    graf.add_edge(15, 12, sign="-")

    graf.add_edge(15, 16, sign="+")
    graf.add_edge(16, 17, sign="+")
    graf.add_edge(17, 18, sign="+")
    graf.add_edge(16, 7, sign="-")
    return graf


# Rucno kreiran neklasterabilan graf
def neklasterabilanGraf():
    graf = nx.Graph()
    for i in range(1, 19):
        graf.add_node(i)
    graf.add_edge(1, 2, sign="+")
    graf.add_edge(1, 3, sign="+")
    graf.add_edge(2, 3, sign="+")

    graf.add_edge(4, 5, sign="+")
    graf.add_edge(3, 4, sign="-")

    graf.add_edge(2, 6, sign="-")
    graf.add_edge(6, 7, sign="-")
    graf.add_edge(7, 8, sign="-")
    graf.add_edge(8, 9, sign="-")

    graf.add_edge(9, 10, sign="+")
    graf.add_edge(9, 11, sign="+")
    graf.add_edge(10, 11, sign="+")
    graf.add_edge(11, 12, sign="+")
    graf.add_edge(11, 14, sign="-")

    graf.add_edge(15, 13, sign="-")
    graf.add_edge(15, 12, sign="-")

    graf.add_edge(15, 16, sign="+")
    graf.add_edge(16, 17, sign="+")
    graf.add_edge(17, 18, sign="+")
    graf.add_edge(16, 18, sign="-")
    graf.add_edge(16, 7, sign="-")
    return graf


# Kreiranje random grafa
def randomGraf():
    klasterabilan = input('-> Da li zelite da random izgenerisan graf bude klasterabilan (y/n)? ')
    while klasterabilan != 'y' and klasterabilan != 'n':
        klasterabilan = input('-> Da li zelite da random izgenerisan graf bude klasterabilan (y/n)? ')
    if (klasterabilan == 'y'):
        res = randomKlasterabilanGraf()
        return res[0]
    if (klasterabilan == 'n'):
        return randomNeklasterabilanGraf()


# Kreiranje random klasterabilnog grafa
def randomKlasterabilanGraf():
    numberOfNodes = input('-> Koliko cvorova zelite da ima random graf? ')
    num_clusters = randint(2, int(int(numberOfNodes)/2))
    p = 0.5
    graph = nx.Graph()
    for n in range(int(numberOfNodes)):
        cluster_num = randint(0, num_clusters)
        graph.add_node(n, cluster=cluster_num)
    for i in graph.nodes:
        for j in graph.nodes:
            if i == j:
                continue
            if graph.nodes[i]['cluster'] == graph.nodes[j]['cluster']:
                if not graph.has_edge(i, j):
                    if random.uniform(0, 1) < p:
                        if graph.degree(i) < 25:
                            graph.add_edge(i, j, sign='+')
            else:
                if random.uniform(0, 1) < p:
                    if graph.degree(i) < 10:
                        graph.add_edge(i, j, sign='-')
    lista = []
    lista.append(graph)
    lista.append(num_clusters)
    return lista


# Kreiranje random neklasterabilnog grafa
def randomNeklasterabilanGraf():
    res_list = randomKlasterabilanGraf()
    graph = res_list[0]
    num_clusters = res_list[1]
    randomlist = random.sample(range(0, num_clusters), int(num_clusters/2))
    for c in randomlist:
        cluster_nodes = [u for u in graph.nodes if graph.nodes[u]['cluster'] == c]
        if len(cluster_nodes) > 3:
            for n in cluster_nodes:
                if graph.degree(n) < 25:
                    neigh = [u for u in nx.neighbors(graph, n) if graph.nodes[u]['cluster'] == c]
                    if len(neigh) >= 2:
                        graph.add_edge(n, neigh[0], sign='+')
                        graph.add_edge(n, neigh[1], sign='+')
                        graph.add_edge(neigh[0], neigh[1], sign='-')
    return graph


def ucitajWiki():
    file = open("wiki-RfA.txt", "r", encoding="utf8")
    graph = nx.DiGraph()
    for line in file:
        if line.startswith("SRC"):
            source = line.split(":")[1]
            if source not in graph.nodes():
                graph.add_node(source)

        if line.startswith("TGT"):
            target = line.split(":")[1]
            if target not in graph.nodes():
                graph.add_node(target)

        if line.startswith("VOT"):
            sign = line.split(":")[1].strip()
            if sign == "1":
                graph.add_edge(source, target, sign=sign)
            elif sign == "-1":
                graph.add_edge(source, target, sign=sign)
    return usmereniUneusmereni(graph)


def ucitajSlashdot():
    file = open('soc-sign-Slashdot081106.txt', "r")
    graph = nx.DiGraph()
    for line in file:
        if not line.startswith('#'):
            row = line.split("\t")
            if row[0].strip() not in graph.nodes:
                graph.add_node(row[0])
            if row[1].strip() not in graph.nodes:
                graph.add_node(row[1])
            graph.add_edge(row[0], row[1], sign=row[2].strip())
    return usmereniUneusmereni(graph)


def ucitajEpinions():
    file = open('soc-sign-epinions.txt', "r")
    graph = nx.DiGraph()
    for line in file:
        if not line.startswith('#'):
            row = line.split()
            if row[0].strip() not in graph.nodes:
                graph.add_node(row[0])
                if row[1].strip() not in graph.nodes:
                    graph.add_node(row[1])
            graph.add_edge(row[0], row[1], sign=row[2].strip())
    return usmereniUneusmereni(graph)


# Kreiranje neusmerenog grafa od ulaznog usmerenog
def usmereniUneusmereni(graph):
    resGraph = nx.Graph()
    resGraph.add_nodes_from(graph.nodes())
    resGraph.add_edges_from(graph.edges(), sign="")
    for u, v, d in graph.edges(data=True):
        afn1 = graph[u][v]['sign']
        afn2 = ""
        if (v, u) in graph.edges:
            afn2 = graph[v][u]['sign']
        if afn1 == "-1" or afn2 == "-1":
            resGraph[u][v]['sign'] = "-"
        else:
            resGraph[u][v]['sign'] = "+"
    return resGraph


# Crtanje grafa
def prikazGrafa(graph):
    print('-> Iscrtavanje grafa.\n')
    if len(graph.nodes) < 200:
        color_map = []
        for node1, node2, data in graph.edges(data=True):
            if data['sign'] == '+':
                color_map.append('green')
            else:
                color_map.append('red')
        tmp = nx.spring_layout(graph)
        nx.draw_networkx_labels(graph, tmp)
        nx.draw_networkx_nodes(graph, tmp, label='True')
        nx.draw_networkx_edges(graph, tmp, edge_color=color_map)
        plt.title('Graf')
        plt.show()
    else:
        print('Graf ima vise od 200 cvorova i nije ga moguce graficki prikazati./n')
