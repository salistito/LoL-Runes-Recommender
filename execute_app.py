import sys
import subprocess

if len(sys.argv) == 3 or len(sys.argv) == 6:

    def run_command(command):
        code = subprocess.call(command)
        print()
        if code != 0:
            print("ERROR EN EL COMANDO!")
            print("(fin de la ejecución)")
            sys.exit()


    def calcular_descriptores_sift(original_images_folder_path, sift_descriptors_folder_path):
        comando = ["python", "sift_descriptors.py", original_images_folder_path, sift_descriptors_folder_path]
        run_command(comando)


    def generar_random_crops(original_images_folder_path, cropped_images_folder_path):
        comando = ["python", "random_crop.py", original_images_folder_path, cropped_images_folder_path]
        run_command(comando)


    def sift_match(sift_descriptors_folder_path, cropped_images_folder_path, results_text_file):
        comando = ["python", "sift_match.py", sift_descriptors_folder_path, cropped_images_folder_path, results_text_file]
        run_command(comando)


    def evaluar_resultados(results_text_file):
        comando = ["python", "evaluator.py", results_text_file]
        run_command(comando)


    def get_runes(cropped_image_path):
        comando = ["python", "get_runes.py", cropped_image_path]
        run_command(comando)

    def app_gui(champ_name, cropped_image_path, result_image_path, runes_sets_json_file):
        comando = ["python", "GUI.py", champ_name, cropped_image_path, result_image_path, runes_sets_json_file]
        run_command(comando)


    def main():
        print("CC5213 - Proyecto Final (2021-2): Recomendación de sets de Runas para campeones de League of Legends")
        execution_mode = sys.argv[1]
        if execution_mode == 'full_execution':
            calcular_descriptores_sift(sys.argv[2], sys.argv[3])
            generar_random_crops(sys.argv[2], sys.argv[4])
            sift_match(sys.argv[3], sys.argv[4], sys.argv[5])
            evaluar_resultados(sys.argv[5])
        elif execution_mode == 'get_runes':
            get_runes(sys.argv[2])


    # método main
    if __name__ == "__main__":
        main()

elif len(sys.argv) != 3 and len(sys.argv) != 6:
    print("La app se puede ejecutar de 2 maneras:")
    print("   En mode='full_execution' o en mode='get_runes'.")
    print("   El modo 'full_execution' sirve para realizar debugging de la app y benchmarking de tiempos.")
    print("   En este modo se precomputan los descriptores sift, se generan crops aleatorios de imágenes")
    print("   se realiza match de vectores sift con un dataset extenso y se anotan los resultados en un archivo .txt")
    print("   El uso es: {} [execution_mode] [original_images_folder_path] [sift_descriptors_folder_path] [cropped_images_folder_path] [results_text_file]".format(sys.argv[0]))
    print()
    print("   El modo 'get_runes' es la app final para los usuarios")
    print("   en donde se ingresa una imagen de un campeón de League of Legends como consulta y se retorna los set de runas adecuados para él")
    print("   El uso es: {} [execution_mode] [cropped_image_path]".format(sys.argv[0]))
    sys.exit(1)
