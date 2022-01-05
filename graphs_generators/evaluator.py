import sys

if len(sys.argv) < 1:
    print("Uso: {} [results_text_file]".format(sys.argv[0]))
    sys.exit(1)

# Almacenar nombre del archivo de texto
results_text_file = sys.argv[1]

# Variables para almacenar la cantidad de respuestas y de respuestas correctas, para sacar un porcentaje de efectividad
ans = 0
correct_ans = 0
# Cargar archivo con los resultados
results = open(results_text_file, "r")  # "r" indica modo lectura
# Leer resultados
lines = results.readlines()[1:]
for line in lines:
    ans += 1
    actual_line = line.split()
    if actual_line[0] == actual_line[1]:
        correct_ans += 1
    else:
        print("Se encontraron errores en:", actual_line)
print("Se obtuvieron {} respuestas correctas de {} dando un porcentaje de {} respuestas correctas".
      format(correct_ans, ans, correct_ans/ans))
results.close()
