import sys
import os
import json
from tkinter import *
from PIL import ImageTk, Image

if len(sys.argv) < 5:
    print("Looking runes for : {} ".format(sys.argv[0]))
    print("Uso: {} [champion_name] [cropped_image_path] [result_image_path] [runes_sets_json_file]".format(sys.argv[0]))
    sys.exit(1)

champion_name = sys.argv[1]
cropped_image_path = sys.argv[2]
result_image_path = sys.argv[3]
runes_sets_json_file = sys.argv[4]

if not os.path.isfile(cropped_image_path):
    print("no existe el archivo {}".format(cropped_image_path))
    sys.exit(1)

if not os.path.isfile(result_image_path):
    print("no existe el archivo {}".format(result_image_path))
    sys.exit(1)

if not os.path.isfile(runes_sets_json_file):
    print("no existe el archivo {}".format(runes_sets_json_file))
    sys.exit(1)


def get_runes(champion_name, runes_sets_json_file):
    with open(runes_sets_json_file) as json_file:
        champions_runes = json.load(json_file)
        champion_runes = champions_runes[champion_name]
        runes_sets = []
        for actual_rune_set in range(1, len(champion_runes)+1):
            runes_sets.append(champion_runes['rune_set{}'.format(actual_rune_set)])
        return runes_sets


def get_rune_set(set, runes_sets_json_file):
    rune_set = runes_sets_json_file[set]
    primary_runes = rune_set["primary_runes"]
    secondary_runes = rune_set["secondary_runes"]
    shards = rune_set["shards"]
    text = 'Primary Runes: \n'
    text += '-> Type: {} \n'.format(primary_runes[0])
    for runes in primary_runes[1]:
        text += '   - {} \n'.format(runes)
    text += ' \n'
    text += 'Secondary Runes: \n'
    text += '-> Type: {} \n'.format(secondary_runes[0])
    for runes in secondary_runes[1]:
        text += '   - {} \n'.format(runes)
    text += ' \n'
    text += 'Shards: \n'
    for shard in shards:
        text += '   - {} \n'.format(shard)
    text += '                             page: {}'.format(set+1)
    return text


# Obtener los sets de runas del campeón encontrado
runes_sets = get_runes(champion_name, runes_sets_json_file)

# create root window
root = Tk()

# root window title and dimension
root.title('Rune Me, LOL runes in a nutshell')
# Set geometry (width x height)
root.geometry('600x580')
root.configure(bg='#49A')
root.resizable(width=False, height=True)

cropped_image_text = Label(root, text='Imagen Ingresada')
cropped_image_text.place(x=10, y=10)

result_image_text = Label(root, text='Campeón Encontrado: {}'.format(champion_name))
result_image_text.place(x=310, y=10)


cropped_image = ImageTk.PhotoImage(Image.open(cropped_image_path).resize((128, 128)))
result_image = ImageTk.PhotoImage(Image.open(result_image_path).resize((405, 239)))

buscado = Label(root, image=cropped_image)
buscado.place(x=10, y=80)  # y=40

resultado = Label(root, image=result_image)
resultado.place(x=210, y=40)

pages = IntVar()
pages.set(0)
runes = Text(root, width=40, height=17)
runes.insert('1.0', get_rune_set(pages.get(), runes_sets))
runes.place(x=150, y=290)


def next_set(pages, rune_text):
    pages.set(pages.get()+1)
    new_rune_set = get_rune_set(pages.get()%4, runes_sets)
    #print(new_rune_set)
    rune_text.delete("1.0", "end")
    rune_text.insert("1.0", new_rune_set)


# button widget with red color text
# inside
btn = Button(root, text="Show me another rune set", command=lambda:next_set(pages, runes))
btn.place(x=450, y=550)

# all widgets will be here
# Execute Tkinter
root.mainloop()
