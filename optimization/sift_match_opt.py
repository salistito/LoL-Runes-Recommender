import sys
import os.path
import cv2
import random
import numpy as np
import time

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


def get_sift_descriptors(descriptor_name, image_path):
    image = cv2.imread(image_path)
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # print("{}: {}".format(descriptor_name, grey_image.shape))
    sift = cv2.SIFT_create()
    keypoints = sift.detect(grey_image)
    keypoints, descriptors = sift.compute(grey_image, keypoints)
    # print("    keypoints={}".format(len(keypoints)))
    # print("    descriptors={} {}".format(descriptors.shape, descriptors.dtype))
    return keypoints, descriptors

def find_matches(descriptors1, descriptors2, threshold_distance):
    bf = cv2.BFMatcher(cv2.NORM_L2)
    matches = bf.match(descriptors1, descriptors2)
    #print("matches encontrados={}".format(len(matches)))
    #ordenar de menor a mayor distancia
    matches = sorted(matches, key=lambda x:x.distance)
    #quedarse solo los menores a cierto umbral
    matches = [m for m in matches if m.distance <= threshold_distance]
    return matches

def comparar_con_distancia_umbral(descriptor_name1, image_path, descriptor_name2, threshold_distance):
    keypoints, descriptors = get_sift_descriptors(descriptor_name1, image_path)
    matches = find_matches(descriptors, descriptor_name2, threshold_distance)
    return matches


# Lista para guardar el resultado (nombre de la imagen original, su posible duplicado y la distancia a este)
result = []
# Iterar sobre el dataset de las imágenes recortadas y sobre el dataset original y encontrar la tupla con mayor matches
for cropped_image in os.listdir(cropped_images_folder_path):
    t0 = time.time()
    #cropped_image1 = random.choice(os.listdir(cropped_images_folder_path))
    print()
    print("Se está buscando a:", cropped_image)
    #print("Se está buscando a:", cropped_image1)
    cropped_image_path = os.path.join(cropped_images_folder_path, cropped_image)
    #cropped_image_path = os.path.join(cropped_images_folder_path, cropped_image1)
    i = 0
    best_matches = 0
    best_champion = ""
    while i < len(os.listdir(sift_descriptors_folder_path))-1:
        sift_descriptors = os.listdir(sift_descriptors_folder_path)[i]
        image_sift_descriptor = np.load(os.path.join(sift_descriptors_folder_path, sift_descriptors))
        matches = comparar_con_distancia_umbral(cropped_image, cropped_image_path, image_sift_descriptor, 150)
        #print("mostrando {} matches menores que cierto umbral".format(len(matches)))
        n_matches = len(matches)
        if n_matches < 3:
            champ_name = sift_descriptors[:-10]
            print(champ_name)
            while champ_name in sift_descriptors:
                i += 1
                sift_descriptors = os.listdir(sift_descriptors_folder_path)[i]
                print(sift_descriptors)
            image_sift_descriptor = np.load(os.path.join(sift_descriptors_folder_path, sift_descriptors))
            matches = comparar_con_distancia_umbral(cropped_image, cropped_image_path, image_sift_descriptor, 150)
            # print("mostrando {} matches menores que cierto umbral".format(len(matches)))
            n_matches = len(matches)
        if n_matches > best_matches:
            best_matches = n_matches
            best_champion = sift_descriptors
            print("El mejor campeón actual es: {0} con {1} matches".format(best_champion, best_matches))
        if best_matches >= 100:
            break
        i += 1
    t1 = time.time()
    dt = t1-t0
    print("el tiempo es:", str(dt))

    result.append([cropped_image, best_champion, best_matches])

# Crear archivo con los resultados
results = open(results_text_file, "w+")  # "w+" indica modo escritura
# Escribir en resultados
for line in result:
    cropped_image, best_champion, best_matches = line
    results.write(f"{cropped_image} \t {best_champion} \t {best_matches}\n")
results.close()
