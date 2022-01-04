import sys
import os.path
import cv2
import numpy as np

if len(sys.argv) < 2:
    print("Uso: {} [original_images_folder_path] [sift_descriptors_folder_path]".format(sys.argv[0]))
    sys.exit(1)

original_images_folder_path = sys.argv[1]
sift_descriptors_folder_path = sys.argv[2]

if not os.path.isdir(original_images_folder_path):
    print("no existe directorio {}".format(original_images_folder_path))
    sys.exit(1)

if not os.path.isdir(sift_descriptors_folder_path):
    print("creando directorio {}".format(sift_descriptors_folder_path))
    os.mkdir(sift_descriptors_folder_path)


def save_sift_descriptors(descriptor_name, image_path):
    image = cv2.imread(image_path)
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    keypoints = sift.detect(grey_image)
    keypoints, descriptors = sift.compute(grey_image, keypoints)
    # print("keypoints={}".format(len(keypoints)))
    # print("descriptors={} {}".format(descriptors.shape, descriptors.dtype))
    np.save(os.path.join(sift_descriptors_folder_path, descriptor_name), descriptors)


for image_name in os.listdir(original_images_folder_path):
    print("Calculando descriptor sift para {}".format(image_name))
    image_path = os.path.join(original_images_folder_path, image_name)
    save_sift_descriptors(image_name, image_path)

