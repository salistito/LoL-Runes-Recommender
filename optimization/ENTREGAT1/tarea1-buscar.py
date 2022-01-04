import sys
import os.path
import numpy as np
import cv2
import math

if len(sys.argv) < 3:
    print("Uso: {} [dataset_q] [datos] [resultados]".format(sys.argv[0]))
    sys.exit(1)

dataset_q =sys.argv[1]
datos = sys.argv[2]
resultados = sys.argv[3]

if not os.path.isdir(dataset_q):
    print("no existe directorio {}".format(dataset_q))
    sys.exit(1)

if not os.path.isdir(datos):
    print("no existe directorio {}".format(datos))
    sys.exit(1)


#se carga el contenido de procesar
for rPath in os.listdir(datos):
    content = np.loadtxt(datos+"/"+rPath,dtype='str')


def getDuplicate(img):
    '''
    Función que recibe una imagen del conjunto q y devuelve
    el nombre de la imagen duplicada y su distancia calculada
    :param img: str -> imagen a buscar
    :return: str , float -> imagen duplicada y distancia
    '''
    result=1000000
    rNameImg="-"
    for rImage in content:
        a=0
        i=1
        while i < len(rImage):
            a+=abs(float(rImage[i])-float(img[i-1]))
            i+=1
        if a < result:
            result=a
            rNameImg=rImage[0]
    return result,rNameImg

#arreglo con el resultado de las imágenes
result = []
#cantidad de zonas a a trabajar
clusters = 5
#cantidad de bins que se le dará a los histogramas
bins=16


for imPath in os.listdir(dataset_q):
    # se obtiene la imagen a buscar
    img = cv2.imread(dataset_q +"/"+ imPath)
    #se inicializa el arreglo np que almacenará los histogramas
    totalIMGHis = np.empty((1, bins))
    #se obtiene el largo o cantidad de filas de la imagen
    largo = len(img)
    #será la cantidad de filas que tendrá cada cluster
    topeFila = math.floor(largo / clusters)


    #se calcula el histograma a cada cluster
    for i in range(clusters):
        imgCuadrante = img[topeFila * i: topeFila * (i + 1)]
        h = cv2.calcHist(imgCuadrante, [0], None, [bins], [0, 256])
        histogramReshape = np.array(h).reshape((1, bins))

        totalIMGHis = np.concatenate((totalIMGHis, histogramReshape[0]), axis=None)

    distance, rImgName = getDuplicate(totalIMGHis)
    result.append([imPath, rImgName, distance])
    print(imPath)


# Se crea el archivo que contendrá los resultados
res = open(resultados, "w+")


# Se escriben los resultados en el archivo de texto
for r in result:
    img1, img2, dist = r
    res.write(f"{img1} \t {img2} \t {dist}\n")

res.close()
