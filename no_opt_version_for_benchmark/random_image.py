import sys
import os.path
import cv2
import random


if len(sys.argv) < 2:
    print("Uso: {} [original_folder_path] [new_folder_path] [number_of_images]".format(sys.argv[0]))
    sys.exit(1)

original_folder_path = sys.argv[1]
new_folder_path = sys.argv[2]
number_of_images = int(sys.argv[3])

if not os.path.isdir(original_folder_path):
    print("no existe directorio {}".format(original_folder_path))
    sys.exit(1)

if not os.path.isdir(new_folder_path):
    print("creando directorio {}".format(new_folder_path))
    os.mkdir(new_folder_path)

for i in range(number_of_images):
    image_name = random.choice(os.listdir(original_folder_path))
    # Obtener imagen a color
    color_image = cv2.imread(os.path.join(original_folder_path, image_name))  # Ej Dimensiones: (320, 500, 3)
    # Guardar imagen aleatoria
    cv2.imwrite(os.path.join(new_folder_path, image_name), color_image)
