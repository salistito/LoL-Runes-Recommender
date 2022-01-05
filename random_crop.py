import sys
import os.path
import cv2
import numpy as np


def get_random_crop(image, crop_height, crop_width):
    """
    Function than generates a random crop of an image passed as parameter
    """
    max_x = image.shape[1] - crop_width
    max_y = image.shape[0] - crop_height
    x = np.random.randint(0, max_x)
    y = np.random.randint(0, max_y)
    crop = image[y: y + crop_height, x: x + crop_width]
    return crop


if len(sys.argv) < 2:
    print("Uso: {} [original_folder_path] [cropped_folder_path]".format(sys.argv[0]))
    sys.exit(1)

original_folder_path = sys.argv[1]
cropped_folder_path = sys.argv[2]

if not os.path.isdir(original_folder_path):
    print("no existe directorio {}".format(original_folder_path))
    sys.exit(1)

if not os.path.isdir(cropped_folder_path):
    print("creando directorio {}".format(cropped_folder_path))
    os.mkdir(cropped_folder_path)

# Limpiar skins del dataset y dejar solo los campeones base
for image_name in os.listdir(original_folder_path):
    # Obtener imagen a color
    color_image = cv2.imread(os.path.join(original_folder_path, image_name))  # Ej Dimensiones: (320, 500, 3)
    # Realizar un recorte aleatorio
    random_crop = get_random_crop(color_image, 256, 256)  # 350
    # Guardar imagen recortada
    cv2.imwrite(os.path.join(cropped_folder_path, image_name), random_crop)
