# LoL-Runes-Recommender


## Para ejecutar la aplicación se debe llamar a `execute_app.py` , acá hay dos modos:

-  El modo 'get_runes' es la app final para los usuarios" en donde se ingresa una 
imagen de un campeón de League of Legends como consulta y se retorna los set de runas 
adecuados para él 
    - El comando de ejecución es: `python execute_app.py get_runes [cropped_image_path]`
    
-El modo 'full_execution' sirve para realizar debugging de la app y benchmarking de tiempos. 
n este modo se precomputan los descriptores sift, se generan crops aleatorios de imágenes 
se realiza match de vectores sift con un dataset extenso y se anotan los resultados en un archivo .txt
    - El comando de ejecución es
    
    `python execute_app.py full_execution [original_images_folder_path] [sift_descriptors_folder_path] [cropped_images_folder_path] [results_text_file]`
    
## Sobre los descriptores del proyecto

Para realizar la comparación entre el screenshot del usuario y el dataset se aplica la detección de 
puntos de interés mediante descriptores SIFT

Los descriptores SIFT calculados para las imágenes del proyecto utilizan el método de diferencias 
gaussianas (Difference of Gaussians). Además al momento de comparar las imágenes de 
los campeones con descriptores locales se restringen los matches entre keypoints, 
seleccionando solos los de menor distancia con respecto a un umbral 
Esto solo funciona con casos "fáciles", cuando la aparición del objeto es muy parecida
 a la consulta, el cual es el caso del proyecto.