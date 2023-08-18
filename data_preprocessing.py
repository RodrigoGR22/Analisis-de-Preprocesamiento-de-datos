import numpy as np
import random
def Vectorizar(dataset, header, col):
    dataT = list(zip(*dataset))
    newHead = list(set(dataT[col]))
    header[col:col + 1] = newHead

    for row in dataset:
        temp = row[col]
        row[col:col + 1] = [0 for i in range(len(newHead))]

        for i in range(col, col + len(newHead)):
            if temp == header[i]:
                row[i] = 1
                break

def ConvertToFloat(data):
    for row in data:
        for pos in range(11,16):
            row[pos] = float(row[pos])

def toFloat(data):
    data_float = []
    for row in data:
        data_float.append(float(row))

    return data_float

def normalizar(dataset):
    dataT = list(zip (* dataset))
    for e in range(11, 16):
        maxV = max(dataT[e])
        minV = min(dataT[e])
        for row in dataset:
            row[e] = 100 * (row[e] - minV) / (maxV - minV)
def estandarizacion(dataset):
    dataT = list(zip (* dataset))
    for e in range(11,16):
        dataT_float = toFloat(dataT[e])
        promedio = np.average(dataT_float)
        stdDev = np.std(dataT_float)
        for row in dataset:
            row[e] = (row[e] - promedio) / stdDev
def convertStr(data):
    for row in range(len(data)):
        for pos in range(len(data[row])):
            data[row][pos] = str(data[row][pos])
def showInCSV(data):
    file = open("gamesSale_process.csv", "w")
    #print(",".join(header))

    file.write(",".join(header) + "\n")
    for row in data:
        #print(",".join(row))
        file.write(",".join(row) + "\n")

def arrangeColumns(pos, h, data):
    h.append(h.pop(pos))

    for d in data:
        d.append(d.pop(pos))

    return h, data
def add_RndData(data):
    columnas = [[fila[11], fila[12], fila[13], fila[14], fila[15]] for fila in data]
    max_list = [max(columna) for columna in columnas]

    random.seed(42)

    for fila, valores in zip(data, columnas):
        for i, valor in enumerate(valores):
            if valor == 0:
                fila[11 + i] = round((random.uniform(0.1, max_list[i])),2)

if __name__ == '__main__':
    file = open("gamesSales.csv", "r")
    dataset = []
    header = file.readline().strip().split(",")
    header[0] = header[0].replace("\ufeff", "")

    for linea in file:
        dataset.append(linea.strip().split(","))

    header.pop(1)
    [d.pop(1) for d in dataset]

    header, dataset = arrangeColumns(3, header, dataset)
    Vectorizar(dataset, header, 1)
    ConvertToFloat(dataset)

    #add_RndData(dataset)

    estandarizacion(dataset)
    normalizar(dataset)

    convertStr(dataset)
    showInCSV(dataset)


