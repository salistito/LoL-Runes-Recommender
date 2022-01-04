import sys
import os.path
import cv2
import numpy as np
import math

if len(sys.argv) < 3:
    print("Uso: {} [dataset_q] [datos] [resultados]".format(sys.argv[0]))
    sys.exit(1)

dataset_q = sys.argv[1]
datos = sys.argv[2]
resultados = sys.argv[3]

if not os.path.isdir(dataset_q):
    print("no existe directorio {}".format(dataset_q))
    sys.exit(1)

if not os.path.isdir(datos):
    print("no existe directorio {}".format(datos))
    sys.exit(1)

# Dimensiones para el resize de las imágenes
width = 10
height = 10
dim = (width, height)
# Secciones en que se dividirá la imagen
sections = 100
# Lista para guardar el resultado (nombre de la imagen original, su posible duplicado y la distancia a este)
result = []

# Cargar descriptores calculados
for image_name in os.listdir(datos):
    images_descriptors = np.load(os.path.join(datos, image_name))

# Función auxiliar para encontrar el mejor duplicado posible (imagen más "cercana" al descriptor)
def get_dulplicatedImage(vector_descriptor):
    original_name = ""  # Nombre de la imagen original asociada al duplicado (aún no hay duplicado -> no hay nombre)
    actual_distance = math.inf  # Distancia actual con respecto al duplicado (aún no se sabe cual es -> big distance)
    for image_descriptor in images_descriptors:  # Iterar sobre los images_descriptors de los posibles duplicados
        duplicate_distance = 0  # Distancia del posible duplicado (inicia en 0)
        for i in range(1, len(image_descriptor)):  # Iterar sobre las componentes del posible duplicado
            duplicate_distance += abs(int(vector_descriptor[i - 1]) - int(image_descriptor[i]))  # Distancia absoluta
        if duplicate_distance < actual_distance:  # Si la distancia es mejor (menor)
            original_name = image_descriptor[0]  # se actualiza el nombre de la imagen original asociada a este duplicado
            actual_distance = duplicate_distance  # se actualiza la distancia al duplicado
    return original_name, actual_distance

# Calcular descriptores para los posibles duplicados
for duplicate_name in os.listdir(dataset_q):
    # Obtener imagen a color
    color_image = cv2.imread(os.path.join(dataset_q, duplicate_name))  # Ej Dimensiones: (320, 500, 3)
    # Pasar a escala de grises
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)  # Ej Dimensiones: (320, 500)
    # Ecualizar imagen
    eq_image = cv2.equalizeHist(gray_image)  # Ej Dimensiones: (320, 500)
    # Realizar resize de la imagen
    resize_image = cv2.resize(eq_image, dim, interpolation=cv2.INTER_CUBIC)  # Ej Dimensiones: (10, 10)
    # Descriptor de la imagen en forma de matriz
    matrix_descriptor = np.array(resize_image)  # Array width x height (10x10)
    # Transformar el descriptor de la imagen en forma de matriz a un vector de 1 dimensión
    vector_descriptor = matrix_descriptor.reshape((1, sections))  # Array 1 x sections (1x100)

    # Obtener posibles duplicados
    original_name, distance = get_dulplicatedImage(vector_descriptor[0])
    result.append([duplicate_name, original_name, distance])

# Crear archivo con los resultados
results = open(resultados, "w+")  # "w+" indica modo escritura
# Escribir en resultados
for line in result:
    duplicate, original, dist = line
    results.write(f"{duplicate} \t {original} \t {dist}\n")
results.close()
