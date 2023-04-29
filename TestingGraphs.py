import networkx as nx
import LoadGraphs as load
import CheckClusterability as clust
import AnalizingGraphs as analize
import sys


def main():
    graph = opcije()
    informacije(graph)
    components = clust.identifyComponents(graph)
    klasteri_podmreze = clust.klasteri_podmreze(components, graph)
    tmp = clust.proveraKlasterabilnosti2(klasteri_podmreze, graph)
    if tmp:
        print('S obzirom da je mreza klasterabilna ne postoje grane koje treba ukloniti.\n')
    else:
        wrong_edges = clust.graneKojeKvareKlasterabilnost1(klasteri_podmreze, graph)
        if len(wrong_edges) > 100:
            print('Bice prikazano samo prvih 100 grana koje treba ukloniti.')
            i = 0
            for e in wrong_edges:
                if i >= 100:
                    break
                print(e)
                i += 1
        else:
            print('-> Grane koje kvare klasterabilnost:')
            for e in wrong_edges:
                print(e)
    koalicije_nekoalicije = clust.koalicije_antikoalicije2(klasteri_podmreze, graph)
    koal = koalicije_nekoalicije[0]
    nekoal = koalicije_nekoalicije[1]
    print('-> Koalicije:')
    for k in koal:
        print(k.nodes)
    print('-> Antikoalicije:')
    for nk in nekoal:
        print(nk.nodes)
    if len(nekoal) > 0:
        analiza_koalicija_antikoalicija(klasteri_podmreze, koal, nekoal)
    mreza_klastera = clust.mreza_klastera(graph, klasteri_podmreze)
    analiza_mreze_klastera(mreza_klastera)
    load.prikazGrafa(graph)
    sys.exit()


def opcije():
    print('Izaberite opciju: \n'
          '1. Klasterabilan graf \n'
          '2. Neklasterabilan graf \n'
          '3. Random graf \n'
          '4. Wiki graf \n'
          '5. Epinions graf \n'
          '6. Slashdot graf')
    opcija = int(input('Unesite neku od ponudjenih opcija:'))
    while opcija > 6 or opcija < 1:
        opcija = int(input('Unesite neku od ponudjenih opcija:'))
    if opcija == 1:
        print('-> Ucitavanje klasterabilnog grafa')
        return load.klasterabilanGraf()
    elif opcija == 2:
        print('-> Ucitavanje neklasterabilnog grafa')
        return load.neklasterabilanGraf()
    elif opcija == 3:
        print('-> Ucitavanje random grafa')
        return load.randomGraf()
    elif opcija == 4:
        print('-> Ucitavanje wiki grafa')
        return load.ucitajWiki()
    elif opcija == 5:
        print('-> Ucitavanje epinions grafa')
        return load.ucitajEpinions()
    elif opcija == 6:
        print('-> Ucitavanje slashdot grafa')
        return load.ucitajSlashdot()


def informacije(graph):
    pos = len([(u, v) for (u, v, d) in graph.edges(data=True) if d['sign'] == "+"])
    neg = len([(u, v) for (u, v, d) in graph.edges(data=True) if d['sign'] == "-"])
    print(neg, "negativnih grana")
    print(pos, "pozitivnih grana")
    print('Broj cvorova: ', len(graph.nodes))
    print('Broj grana: ', len(graph.edges))
    print('Broj povezanih komponenti u mrezi: ', nx.number_connected_components(graph))
    giant = analize.giantComponent(graph)
    print('Indeks asortativnosti pocetnog grafa: ', nx.degree_assortativity_coefficient(graph))


def findGraph(klaster, klasteri):
    for k in klasteri:
        if k.nodes == klaster.nodes:
            return k


def analiza_koalicija_antikoalicija(klasteri_podmreze, koal, nekoal):
    print('-> Analiza koalicija i antikoalicija')
    res_koalicije = [[] for i in range(3)]
    res_antikoalicije = [[] for i in range(3)]

    for k in koal:
        podgraf = findGraph(k, klasteri_podmreze)
        res_koalicije = analize.analiza_koalicija_antikoalicija(podgraf, res_koalicije)

    for nk in nekoal:
        podgraf = findGraph(nk, klasteri_podmreze)
        res_antikoalicije = analize.analiza_koalicija_antikoalicija(podgraf, res_antikoalicije)

    # if (sum(res_antikoalicije[0])/len(res_antikoalicije[0])) > (sum(res_koalicije[0])/len(res_koalicije[0])):
    #     print('Indeks asortativnosti antikoalicija je veci od indeksa asortativnosti koalicija.')
    # elif (sum(res_antikoalicije[0])/len(res_antikoalicije[0])) < (sum(res_koalicije[0])/len(res_koalicije[0])):
    #     print('Indeks asortativnosti antikoalicija je manji od indeksa asortativnosti koalicija.')
    # else:
    #     print('Indeks asortativnosti antikoalicija je jednak sa indeksom asortativnosti koalicija.')

    if (sum(res_antikoalicije[0])/len(res_antikoalicije[0])) > (sum(res_koalicije[0])/len(res_koalicije[0])):
        print('Prosecan stepen antikoalicija je veci od prosecnog stepena koalicija.')
    elif (sum(res_antikoalicije[0])/len(res_antikoalicije[0])) < (sum(res_koalicije[0])/len(res_koalicije[0])):
        print('Prosecan stepen antikoalicija je manji od prosecnog stepena koalicija.')
    else:
        print('Prosecan stepen antikoalicija je jednak sa prosecnim stepenom koalicija.')

    if (sum(res_antikoalicije[1])/len(res_antikoalicije[1])) > (sum(res_koalicije[1])/len(res_koalicije[1])):
        print('Gustina antikoalicija je veca od gustine koalicija.')
    elif (sum(res_antikoalicije[1])/len(res_antikoalicije[1])) < (sum(res_koalicije[1])/len(res_koalicije[1])):
        print('Gustina antikoalicija je manja od gustine koalicija.')
    else:
        print('Gustina antikoalicija je jednaka sa gustinom koalicija.')


def analiza_mreze_klastera(mreza_klastera):
    print('-> Analiza mreze klastera')
    print('Broj komponenti povezanosti: ', nx.number_connected_components(mreza_klastera))
    print('Prosecan stepen cvorova mreze: ', analize.averageDegree(mreza_klastera))
    print('Gustina mreze: ', analize.density(mreza_klastera))
    print('Indeks asortativnosti mreze: ', analize.asortativnost(mreza_klastera))
    d = analize.dijametarGrafa(mreza_klastera)
    if d == 0:
        print('Nije moguce odrediti dijametar mreze, jer ima vise od jedne komponente povezanosti.',)
    else:
        print('Dijametar mreze: ', d)


if __name__ == '__main__':
    main()
