import sys
import os.path
import cv2
import numpy as np
import time
import random

if len(sys.argv) < 3:
    print("Uso: {} [sift_descriptors_folder_path] [cropped_images_folder_path] [results_text_file]".format(sys.argv[0]))
    sys.exit(1)

sift_descriptors_folder_path = sys.argv[1]
cropped_images_folder_path = sys.argv[2]
results_text_file = sys.argv[3]

if not os.path.isdir(sift_descriptors_folder_path):
    print("no existe directorio {}".format(sift_descriptors_folder_path))
    sys.exit(1)

if not os.path.isdir(cropped_images_folder_path):
    print("no existe directorio {}".format(cropped_images_folder_path))
    sys.exit(1)


def get_sift_descriptors(image_path):
    image = cv2.imread(image_path)
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    keypoints = sift.detect(grey_image)
    keypoints, descriptors = sift.compute(grey_image, keypoints)
    ##print("keypoints={}".format(len(keypoints)))
    ##print("descriptors={} {}".format(descriptors.shape, descriptors.dtype))
    return descriptors


def find_matches(descriptors1, descriptors2, threshold_distance):
    bf = cv2.BFMatcher(cv2.NORM_L2)
    matches = bf.match(descriptors1, descriptors2)
    ##print("matches encontrados={}".format(len(matches)))
    #ordenar de menor a mayor distancia
    matches = sorted(matches, key=lambda x:x.distance)
    #quedarse solo los menores a cierto umbral
    matches = [m for m in matches if m.distance <= threshold_distance]
    return matches


def comparar_con_distancia_umbral(descriptor_name1, descriptor_name2, threshold_distance):
    return find_matches(descriptor_name1, descriptor_name2, threshold_distance)


# Arreglo que guarda el resultado (imagen de consulta, imagen detectada, confianza o n° matches y tiempo de consulta)
result = [["Img Consulta", "Img Detectada", "Matches", "Tiempo"]]

# Iterar sobre el dataset de las imágenes recortadas y sobre el dataset original y encontrar la tupla con mayor matches
for cropped_image in os.listdir(cropped_images_folder_path):
    t0 = time.time()
    print("\nSe está buscando a:", cropped_image)
    cropped_image_path = os.path.join(cropped_images_folder_path, cropped_image)
    ##cropped_image1 = random.choice(os.listdir(cropped_images_folder_path))
    ##print("\nSe está buscando a:", cropped_image1)
    ##cropped_image_path = os.path.join(cropped_images_folder_path, cropped_image1)
    cropped_image_sift_descriptors = get_sift_descriptors(cropped_image_path)
    best_matches = 0
    best_champion = ""
    for sift_descriptors in os.listdir(sift_descriptors_folder_path):
        original_image_sift_descriptor = np.load(os.path.join(sift_descriptors_folder_path, sift_descriptors))
        matches = comparar_con_distancia_umbral(cropped_image_sift_descriptors, original_image_sift_descriptor, 150)
        n_matches = len(matches)
        ##print("mostrando {} matches menores que cierto umbral".format(len(matches)))
        if n_matches > best_matches:
            best_matches = n_matches
            best_champion = sift_descriptors[:-4]  # Quitar extensión .npy y dejar el nombre de la imagen del campeón
            #print("El mejor campeón actual es: {0} con {1} matches".format(best_champion, best_matches))
        if best_matches >= 100:
            break
    dt = time.time()-t0
    #print("el tiempo de consulta fue:", str(dt))
    result.append([cropped_image, best_champion, best_matches, dt])

# Crear archivo con los resultados
results = open(results_text_file, "w+")  # "w+" indica modo escritura
# Escribir en resultados
for line in result:
    cropped_image, best_champion, best_matches, dt = line
    results.write(f"{cropped_image} \t {best_champion} \t {best_matches} \t {dt}\n")
results.close()
