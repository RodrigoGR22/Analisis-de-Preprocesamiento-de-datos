import math
import random as rand
import matplotlib.pyplot as plt


def distf(dsRow, CRow):
    global a
    sum = 0
    for j in range(a):
        sum += (dsRow[j] - CRow[j]) ** 2
    return sum


def encuentraGrupos():
    modEnGrupo = False
    for i in range(len(G)):  # G = [-1,-1,-1....-1]
        distMin = 99999999
        lMin = -1

        for l in range(k):
            # print(ds[i], '  --------  ', C[l])
            dist = distf(ds[i], C[l])

            if dist < distMin:
                distMin = dist
                lMin = l

        if G[i] != lMin:
            modEnGrupo = True
            G[i] = lMin

    return G, modEnGrupo


def actualizarCentroides():
    cont = [0 for i in range(k)]

    for i in range(n):
        cont[G[i]] += 1
        for j in range(a):
            C[G[i]][j] += ds[i][j]

    for i in range(k):
        for j in range(a):
            if cont[i] == 0:
                C[i][j] = 0
            else:
                C[i][j] /= cont[i]

    return C


def findColor(group):
    global colors
    return colors[group]


def Graph():
    global G, C
    listColors = list(map(findColor, G))
    fig, ax = plt.subplots()
    ax.scatter(dsT[0], dsT[1], c=listColors)
    CT = list(zip(*C))
    ax.scatter(CT[0], CT[1], color="red")
    plt.show()


def convertFloat(vector, pos_min, pos_max):
    for v in range(pos_min, pos_max):
        vector[v] = float(vector[v])


def convertInt(vector, pos_min, pos_max):
    for v in range(pos_min, pos_max):
        vector[v] = int(vector[v])


def Lectura(name, WithNames=False, WithHeaders=False, separator=","):
    f = open(name)

    cabecera = f.readline().strip().split(",")
    cabecera[0] = cabecera[0].replace("\ufeff", "")

    del (cabecera[0:10])
    cabecera.pop(-1)

    nombres = []
    ds = []
    start = 0

    for linea in f:
        linea = linea.strip()
        lineaList = linea.split(separator)

        if WithNames:
            nombres.append(lineaList[0])
            start = 1
        else:
            nombres.append(linea)

        ds.append([])

        for i in range(start, len(lineaList)):
            ds[-1].append((lineaList[i]))
        [convertInt(e, 0, 9) for e in ds]
        [convertFloat(e, 10, 15) for e in ds]

    return cabecera, nombres, ds


def InitializeC(list_ds, list_dsT):
    C = [[0 for j in range(len(list_ds[0]))] for i in range(k)]

    for i in range(len(C)):
        for j in range(5):
            maxV = math.ceil((max)(list_dsT[j]))
            minV = math.floor((min)(list_dsT[j]))
            C[i][j] = rand.randint(minV, maxV)
    return C


def PrintToFile(cabecera, nombres, ds, G):
    file = open("Resultado.txt", "w")

#    file.write(cabecera.replace(",", "\t").replace("\n", "\t") + "\tGrupo\n")
    file.write(",".join(cabecera) + "\t" + "Grupo\n")
    for i in range(len(ds)):
        file.write(nombres[i] + "\t" + "\t".join([str(round(x, 2)) for x in ds[i]]) + "\t" + str(G[i]) + "\n")
    file.close()


if __name__ == '__main__':
    continuar = True

    cabecera, nombres, ds = Lectura("gamesSale_process.csv", WithHeaders=True, WithNames=True, separator=",")

    n = len(ds)

    # gruposReales = [int(x[-1]) for x in ds]

    grupos = []

    for row in ds:
        grupos.append(row.pop(-1))
        del (row[0:10])
        a = len(ds[0])
    dsT = list(zip(*ds))

    k = 3
    C = InitializeC(ds, dsT)
    print('C 1: ', C)

    G = [-1 for x in range(n)]

    colors = dict()
    sumColor = 50

    for group in range(0, k):
        colors.setdefault(group, sumColor)
        sumColor += 50

    max_iteraciones = 10
    iteraciones = 0

    while continuar and iteraciones < max_iteraciones:
        continuar = False
        G, continuar = encuentraGrupos()

        C = actualizarCentroides()
        print(C)
        Graph()
        iteraciones += 1

PrintToFile(cabecera, nombres, ds, G)
