import sys
import os.path

if len(sys.argv) < 1:
    print("Uso: {} [folder_path]".format(sys.argv[0]))
    sys.exit(1)

folder_path = sys.argv[1]

if not os.path.isdir(folder_path):
    print("no existe directorio {}".format(folder_path))
    sys.exit(1)
    
# Limpiar skins del dataset y dejar solo los campeones base
for image_name in os.listdir(folder_path):
    if "_0" not in image_name:
        os.remove(folder_path + image_name)
print(len(os.listdir(folder_path)))
