import networkx as nx
from itertools import combinations

visited = []
components = []
coalitions = []
anti_coalitions = []
num_coalition = []


def identifyComponents(graph):
    print('-> Identifikovanje klastera u mrezi')
    component = 0
    for node in graph.nodes:
        if node not in visited:
            components.append(bfs(node, graph))
            component += 1
    print('-> Broj klastera u mrezi: ', component)
    return components


def bfs(node, graph):
    comp = []
    queue = []
    comp.append(node)
    visited.append(node)
    queue.append(node)
    while queue:
        current = queue.pop(0)
        neighbors = nx.neighbors(graph, current)
        for n in neighbors:
            sign = graph.get_edge_data(current, n)
            if sign['sign'] == '-':
                continue
            if n not in visited:
                comp.append(n)
                visited.append(n)
                queue.append(n)
    return comp


# prosledjujemo listu komponenti gde svaki klaster predstavlja jedan podgraf
# proveravamo da li u svakom od podgrafa postoji negativna grana
# ukoliko postoji dodamo u listu
def graneKojeKvareKlasterabilnost1(components, graph):
    print('->Identifikacija grana koje kvare klasterabilnost.')
    wrong_edges = []
    for c in components:
        neg_edges = [(u, v) for (u, v, d) in c.edges(data=True) if d['sign'] == "-"]
        if len(neg_edges) > 0:
            wrong_edges.extend(neg_edges)
    print('Broj grana koje kvare klasterabilnost: ', len(wrong_edges))
    return wrong_edges


# metodama se prosledjuje lista klustera koji su predstavljeni zasebnim podgrafom
def proveraKlasterabilnosti2(components, graph):
    print('-> Provera klasterabilnosti mreze')
    for c in components:
        neg_edges = [(u, v) for (u, v, d) in c.edges(data=True) if d['sign'] == "-"]
        if len(neg_edges) > 0:
            print('Mreza nije klasterabilna, postoje negativne grane/grana u nekom od klastera.')
            return False
    print('Mreza jeste klasterabilna, ne postoje negativne grane unutar klastera.')
    return True


def koalicije_antikoalicije2(components, graph):
    print('-> Pretraga koalicija i antikoalicija')
    coalitions = []
    anti_coalitions = []
    res = []
    for c in components:
        neg_edges = [(u, v) for (u, v, d) in c.edges(data=True) if d['sign'] == "-"]
        if len(neg_edges) > 0:
            anti_coalitions.append(c)
        else:
            coalitions.append(c)
    print('Broj koalicija: ', len(coalitions))
    print('Broj antikoalicija: ', len(anti_coalitions))
    res.append(coalitions)
    res.append(anti_coalitions)
    return res


def klasteri_podmreze(clusters, graph):
    print('-> Kreiranje podgrafa za svaki klaster')
    podmreza = []
    for cluster in clusters:
        g = nx.Graph()
        for node in cluster:
            g.add_node(node)
        comb = list(combinations(cluster, 2))
        for c in comb:
            if graph.has_edge(c[0], c[1]):
                edge = graph.get_edge_data(c[0], c[1])['sign']
                g.add_edge(c[0], c[1], sign=edge)
            else:
                continue
        podmreza.append(g)
    return podmreza


def mreza_klastera(graph, clusters):
    print('-> Konstruisanje mreze klastera')
    novi_graf = nx.Graph()
    for k in clusters:
        k.graph['nodes'] = str(k.nodes)
        novi_graf.add_node(k.graph['nodes'])

    for k1 in clusters:
        for k2 in clusters:
            if k1 == k2:
                continue
            povezani = False
            br = 0
            nodes_k1 = list(k1.nodes)
            while br < len(k1.nodes):
                n1 = nodes_k1[br]
                br += 1
                for n2 in k2:
                    if n1 in nx.neighbors(graph, n2):
                        povezani = True
                        br = len(k1.nodes)+1
            if povezani:
                novi_graf.add_edge(k1.graph['nodes'], k2.graph['nodes'], sign='-')
    print('Broj cvorova u mrezi klastera: ', len(novi_graf.nodes()))
    print('Broj grana u mrezi klastera: ', len(novi_graf.edges()))
    return novi_graf


# metode koje se ne koriste u programu

# prosledjujemo listu komponenti koje su predstavljene listom cvorova
# za svaku komponentu pravimo sve moguce kombinacije grana i kontrolisemo
# koje grane postoje u grafu i da li postoji neka negativna u komponenti
def graneKojeKvareKlasterabilnost(components, graph):
    neg_edges = [(u, v) for (u, v, d) in graph.edges(data=True) if d['sign'] == "-"]
    wrong_edges = []
    for c in components:
        if len(c) > 1:
            comb = list(combinations(c, 2))
            for c1 in comb:
                if c1 in neg_edges:
                    wrong_edges.append(c1)
    print('Broj grana koje kvare klasterabilnost: ', len(wrong_edges))
    return wrong_edges


# za svaki klaster se zasebno kreira podmreza
def proveraKlasterabilnosti1(components, graph):
    for c in components:
        k = kreirajKlaster(c, graph)
        neg_edges = [(u, v) for (u, v, d) in k.edges(data=True) if d['sign'] == "-"]
        if len(neg_edges) > 0:
            return True
    return False


def koalicije_antikoalicije1(components, graph):
    coalitions = []
    anti_coalitions = []
    res = []
    for c in components:
        k = kreirajKlaster(c, graph)
        neg_edges = [(u, v) for (u, v, d) in k.edges(data=True) if d['sign'] == "-"]
        if len(neg_edges) > 0:
            anti_coalitions.append(c)
        else:
            coalitions.append(c)
    print('Broj koalicija: ', len(coalitions))
    print('Broj antikoalicija: ', len(anti_coalitions))
    res.append(coalitions)
    res.append(anti_coalitions)
    return res


def kreirajKlaster(cluster, graph):
    g = nx.Graph()
    for node in cluster:
        g.add_node(node)
    comb = list(combinations(cluster, 2))
    for c in comb:
        if graph.has_edge(c[0], c[1]):
            edge = graph.get_edge_data(c[0], c[1])['sign']
            g.add_edge(c[0], c[1], sign=edge)
        else:
            continue
    return g
