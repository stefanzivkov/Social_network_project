import networkx as nx


def averageDegree(g):
    return (len(g.edges)*2)/len(g.nodes)


def density(g):
    # avg_degree = averageDegree(g)
    # return avg_degree / (len(g.nodes)-1)
    return nx.density(g)


def giantComponent(g):
    Gcc = sorted(nx.connected_components(g), key=len, reverse=True)
    giant = Gcc[0]
    print('Gigantska komponenta povezanosti cini ', (len(Gcc[0])/len(g.nodes))*100, '% cvorova grafa.')
    return giant


def asortativnost(g):
    return nx.degree_assortativity_coefficient(g)


def dijametarGrafa(g):
    komponente = nx.number_connected_components(g)
    if komponente > 1:
        return 0
    else:
        return nx.diameter(g)


def analiza_koalicija_antikoalicija(klaster, res):
    # asort = asortativnost(klaster)
    # res[0].append(asort)
    avgDeg = averageDegree(klaster)
    res[0].append(avgDeg)
    d = density(klaster)
    res[1].append(d)
    return res
