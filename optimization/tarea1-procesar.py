import sys
import os.path
import cv2
import numpy as np

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

# Dimensiones para el resize de las imágenes
width = 10
height = 10
dim = (width, height)
# Secciones en que se dividirá la imagen
sections = 100

# Arreglo para guardar la información de los descriptores (vectores)
vectors = np.empty((1, sections+1))  # Inicialmente es de 1x101 para poder concatenarlo con los descriptores de 1x101

# Calcular descriptores
for image_name in os.listdir(dataset_r):
    # Obtener imagen a color
    color_image = cv2.imread(os.path.join(dataset_r, image_name))  # Ej Dimensiones: (320, 500, 3)
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

    # Concatenar el nombre de la foto al vector que la describe
    image_descriptor = np.concatenate(([image_name], vector_descriptor[0])).reshape((1, sections + 1))  # Array 1 x sections+1 (1x101)
    # Concatenar el resultado al vector con la información de este dataset
    vectors = np.concatenate((vectors, image_descriptor), axis=0)  # Al final de la iteración -> Dimensiones: 1000x101
    
# Escribir en datos
vectors = np.delete(vectors, 0, axis=0)  # Eliminar primera fila que se dejó para poder realizar la concatenación
vectors_filename = "images_descriptors"
np.save(os.path.join(datos, "images_descriptors"), vectors)
