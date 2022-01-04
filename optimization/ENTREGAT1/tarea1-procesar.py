import sys
import os.path
import cv2
import numpy as np
import math

if len(sys.argv) < 2:
    print("Uso: {} [dataset_r] [datos]".format(sys.argv[0]))
    sys.exit(1)

dataset_r = sys.argv[1]
datos = sys.argv[2]

if not os.path.isdir(dataset_r):
    print("no existe directorio {}".format(dataset_r))
    sys.exit(1)

if not os.path.isdir(datos):
    print("creando directorio {}".format(datos))
    os.mkdir(datos)

# calcular descriptores
# escribir en datos

dir_salida = "datos_calculados_R"

# bins a utilizar en el histograma de cada cluster
bins = 16
# cantidad de clusters
clusters = 5
# se inicializa el arreglo de numpy que guardará la info de cada imagen en r
totalHis = np.empty((1, bins * (clusters + 1) + 1))

# se recorren las imagenes en imagenes_r
for imPath in os.listdir(dataset_r):
    # se inicializa el vector que almacena el conjunto de histogramas
    totalIMGHis = np.empty((1, bins))
    # se lee la imagen
    img = cv2.imread(dataset_r + "/" + imPath)
    # se obtiene el largo de la imagen
    largo = len(img)
    # se calcula el largo de cada cluster
    topeFila = math.floor(largo / clusters)

    # se calculan los histogramas en cada cluster
    for i in range(clusters):
        # se obtienen los respectivos datos
        imgCuadrante = img[topeFila * i: topeFila * (i + 1)]

        h = cv2.calcHist(imgCuadrante, [0], None, [bins], [0, 256])
        histogramReshape = np.array(h).reshape((1, bins))
        # se concatena con los demas histogramas
        totalIMGHis = np.concatenate((totalIMGHis, histogramReshape[0]), axis=None)

    # se concatena en nombre de la imagen con su descriptor
    inResult = np.concatenate(([imPath], totalIMGHis),
                              axis=None).reshape((1, bins * (clusters + 1) + 1))

    # se concatena el arreglo de la imagen al arreglo que almacena todos los valores
    totalHis = np.concatenate((totalHis, inResult))

# se elimina la primera linea
r = totalHis[1:]
# se guardan los datos
np.savetxt(datos + "/" + dir_salida + ".txt", r, fmt='%s')