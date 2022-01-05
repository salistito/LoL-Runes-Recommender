import matplotlib.pyplot as plt
import sys
import os
import numpy as np

if len(sys.argv) < 1:
    print("Uso: {} [results_text_file]".format(sys.argv[0]))
    sys.exit(1)


## Run with
## python evaluators/graphics_splash_results.py Results/splash_results.txt

result_path=sys.argv[1]

if not os.path.isfile(result_path):
    print("No existe el archivo{}".format(result_path))
    sys.exit(1)

def getContent(file):
    """
    Función que recibe la ruta de un archivo y carga su contenido en
    un array de numpy
    :param file: ruta del archivo txt
    :return: numpy array
    """
    return np.genfromtxt(file,delimiter='\t',dtype=str)




results = getContent(result_path) # "r" indica modo lectura

def getDatatoPlot(result):
    champions=[]
    matches=[]
    time=[]
    for row in result[1:]:
        champions.append(row[0][0])
        matches.append(float(row[2]))
        time.append(float(row[3]))
    return[champions,matches,time]

graphicInfo=getDatatoPlot(results)

def makeGraphic(x,y,title,label='',xlabel='',ylabel='',color='r',linestyle='', marker='o', markerfacecolor='c'):
    plt.plot(x,y,label=label,color=color,linestyle=linestyle, marker=marker, markerfacecolor=markerfacecolor)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plt.xlim(0,100)
    #plt.ylim(0,100)
    plt.title(title)
    plt.legend()
    plt.show()

#makeGraphic(graphicInfo[0],graphicInfo[1],'Matches per Champion Initial','matches','Inicial campeon%','n° matches')
#makeGraphic(graphicInfo[0],graphicInfo[2],'Time per Champion Initial','time','Inicial campeon%','time s%')
#print(results)

figure, axis = plt.subplots(2, 1)
figure.suptitle('Time and matches per champion initial- Optimized , splash dataset', fontsize=14)
axis[0].plot(graphicInfo[0],graphicInfo[1],linestyle='', marker='o')
axis[0].set_title("Matches per Champion Initial")

axis[1].plot(graphicInfo[0],graphicInfo[2],linestyle='', marker='o')
axis[1].set_title("Time per Champion Initial")

plt.savefig(result_path[:-4])
plt.show()

