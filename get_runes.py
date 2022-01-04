import sys
import os.path
import cv2
import numpy as np
import subprocess
import json

if len(sys.argv) < 2:
    print("Uso: {} [cropped_image_path]".format(sys.argv[0]))
    sys.exit(1)

sift_descriptors_folder_path = "splash_sift_descriptors"
cropped_image_path = sys.argv[1]
original_images_path = "dragontail-11.24.1\\img\\champion\\splash"

if not os.path.isdir(sift_descriptors_folder_path):
    print("no existe directorio {}".format(sift_descriptors_folder_path))
    sys.exit(1)


def get_sift_descriptors(image_path):
    image = cv2.imread(image_path)
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    keypoints = sift.detect(grey_image)
    keypoints, descriptors = sift.compute(grey_image, keypoints)
    return descriptors


def find_matches(descriptors1, descriptors2, threshold_distance):
    bf = cv2.BFMatcher(cv2.NORM_L2)
    matches = bf.match(descriptors1, descriptors2)
    #ordenar de menor a mayor distancia
    matches = sorted(matches, key=lambda x:x.distance)
    #quedarse solo los menores a cierto umbral
    matches = [m for m in matches if m.distance <= threshold_distance]
    return matches


def comparar_con_distancia_umbral(descriptor_name1, descriptor_name2, threshold_distance):
    return find_matches(descriptor_name1, descriptor_name2, threshold_distance)


def print_rune_set(json_file):
    primary_runes = json_file["primary_runes"]
    secondary_runes = json_file["secondary_runes"]
    shards = json_file["shards"]
    print(f"Primary Runes \n{primary_runes[0]}")  # Rama principal
    for runes in primary_runes[1]:
        print(runes)
    print(f"\nSecondary Runes \n{secondary_runes[0]}")  # Rama secundaria
    for runes in secondary_runes[1]:
        print(runes)
    print("\nShards")  # Fragmentos de runas
    for shard in shards:
        print(shard)  # Obtener el nombre correspondiente al fragmento
    print("===========================================================")


def app_gui(champ_name, cropped_image_path, result_image_path, runes_sets_json_file):
    comando = ["python", "GUI.py", champ_name, cropped_image_path, result_image_path, runes_sets_json_file]
    subprocess.call(comando)


print("\nSe está buscando a:", cropped_image_path)
cropped_image_sift_descriptors = get_sift_descriptors(cropped_image_path)
best_matches = 0
best_result_image = ""
for sift_descriptors in os.listdir(sift_descriptors_folder_path):
    original_image_sift_descriptor = np.load(os.path.join(sift_descriptors_folder_path, sift_descriptors))
    matches = comparar_con_distancia_umbral(cropped_image_sift_descriptors, original_image_sift_descriptor, 150)
    n_matches = len(matches)
    if n_matches > best_matches:
        best_matches = n_matches
        best_result_image = sift_descriptors[:-4]  # Quitar extensión .npy y dejar el nombre de la imagen del campeón
        #print("El mejor campeón actual es: {0} con {1} matches".format(best_champion, best_matches))
    if best_matches >= 100:
        break
_index = best_result_image.index('_')
champion_name = best_result_image[:_index]
best_result_image_path = os.path.join(original_images_path, best_result_image)
#print("El mejor campeón encontrado fue: {0} con {1} matches".format(champion_name, best_matches))
#print("===========================================================")
"""
with open('champions_runes.json') as json_file:
    champions_runes = json.load(json_file)
    champion_runes = champions_runes[champion_name]
    for actual_rune_set in range(1, len(champion_runes)+1):
        print("Runeset {0}:".format(actual_rune_set))
        rune_set = champion_runes['rune_set{}'.format(actual_rune_set)]
        print_rune_set(rune_set)
"""
app_gui(champion_name, cropped_image_path, best_result_image_path, "champions_runes.json")
