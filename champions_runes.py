from urllib import request
from urllib.request import Request
from bs4 import BeautifulSoup
import json


def get_champions_names():
    """
    Returns a list with the names of all playable champions in League of Legends
    """
    champions = []
    URL = "https://www.leagueoflegends.com/en-us/champions/"
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50'}
    req = Request(URL, headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, "html.parser")  # Formato beautifulsoup para ir obteniendo elementos html
    champions_spans = soup.find_all('span', class_="style__Text-n3ovyt-3 gMLOLF")
    for champion_span in champions_spans:
        champion_name = champion_span.text
        normalized_name = champion_name.replace(" ", "").replace("'", "").replace(".", "")  # Limpiar espacios, comillas y puntos
        champions.append(normalized_name)
    return champions


def get_champion_runes(champion, lane="all"):
    """
    Gets the runes of specific champion on his principal lane
    """
    rune_options = []
    URL = "https://na.op.gg/champion/" + champion + "/statistics/" + lane
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50'}
    req = Request(URL, headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, "html.parser")  # Formato beautifulsoup para ir obteniendo elementos html
    # op.gg entrega 4 recomendaciones de sets de runas.
    # 2 sets con la combinación de ramas más popular y los otros 2 sets con la segunda combinación de ramas más popular.
    paths = soup.find_all('div', class_="champion-stats-summary-rune__name")  # Las ramas que sigue un set de runas, ej: Precision + Domination
    rune_paths = ([path.text.split(' + ') for path in paths])  # Tupla con las ramas de los set de runas, ej: [['Precision', 'Domination'], ['Sorcery', 'Inspiration']]
    active_runes = soup.find_all('div', class_=["perk-page__item perk-page__item--active",\
                                                  "perk-page__item perk-page__item--keystone perk-page__item--active"])  # Runas activas dentro de las ramas principales
    
    # Determine the Primary/Secondary runes for each set
    all_runes = []  # Runas activas de los 4 sets de runas
    for runes in active_runes:
        all_runes.append(runes.find('img', alt=True)['alt'])  # Obtener el atributo alt de las runas activas (la descripción en texto de la imagen de la runa activa)
    
    # Determine the shards for each set
    all_shards = []  # Fragmentos activos de los 4 sets de runas
    active_shards = soup.find_all('div', class_="fragment__detail")  # fragmentos de cada set de runas
    for i in range(len(active_shards)):  # op.gg entrega 4 recomendaciones de sets de runas (for del 0 al 3)
        shard_option = active_shards[i].find_all('div', class_="fragment__row")  # las 3 rows de los fragmentos por cada set de runas
        _shard = []
        for j in range(len(shard_option)):  # iterar sobre las 3 rows y sacar el fragmento activo
            for k in range(3):  # dentro de cada row iterar sobre las 3 opciones y sacar el fragmento activo
                if ('class="active tip"' in str(shard_option[j].find_all('img')[k])):
                    _shard.append(k)

    # TODO: clean up data processing. op.gg seems always have 4 options but that could change
    # Formats data into a list of all runes
    # Datos:
    # cada set de runas tiene 6 runas
    # la rama principal de un set de runas tiene 4 runas
    # la rama secundaria de un set de runas tiene 2 runas
        if i in [0, 1]:  # Los 2 sets con la combinación de ramas más popular
            primary_path = [rune_paths[0][0], all_runes[(6*i):(4+(i*6))]]  # Obtener las 4 runas de la rama principal
            secondary_path = [rune_paths[0][1], all_runes[4+(6*i):(6+(i*6))]]  # Obtener las 2 runas de la rama secundaria
            rune_options.append([primary_path, secondary_path, _shard])
        else:  # los otros 2 sets con la segunda combinación de ramas más popular.
            primary_path = [rune_paths[1][0], all_runes[(6*i):(4+(i*6))]]  # Obtener las 4 runas de la rama principal
            secondary_path = [rune_paths[1][1], all_runes[4+(6*i):(6+(i*6))]]  # Obtener las 2 runas de la rama secundaria
            rune_options.append([primary_path, secondary_path, _shard])
    return(rune_options)


def display(rune_options):
    """
    Displays runes of a specific champion and lane
    """
    shard_rows = ['Offense Adaptive Force +9', 'Offense +10% Attack Speed', 'Offense +1-10% CDR (based on level)'],\
                 ['Offense Adaptive Force +9', 'Flex +6 Armor', 'Flex +8 Magic Resist'],\
                 ['Defense +15-90 Health (based on level)', 'Flex +6 Armor', 'Flex +8 Magic Resist']
    for rune_set in rune_options:  # Iterar sobre las 4 opciones de sets de runas
        print(f"Primary Runes \n{rune_set[0][0]}")  # Rama principal
        for runes in rune_set[0][1]:
            print(runes)
        print(f"\nSecondary Runes \n{rune_set[1][0]}")  # Rama secundaria
        for runes in rune_set[1][1]:
            print(runes)
        print("\nShards")  # Fragmentos de runas
        for shard in range(len(rune_set[2])):
            print(shard_rows[shard][rune_set[2][shard]])  # Obtener el nombre correspondiente al fragmento
        print("===========")


def generate_json_runes():
    champion_runes = {}
    shard_rows = ['Offense Adaptive Force +9', 'Offense +10% Attack Speed', 'Offense +1-10% CDR (based on level)'],\
                 ['Offense Adaptive Force +9', 'Flex +6 Armor', 'Flex +8 Magic Resist'],\
                 ['Defense +15-90 Health (based on level)', 'Flex +6 Armor', 'Flex +8 Magic Resist']
    for champion in get_champions_names():
        print(champion)
        champion_runes[champion] = {"rune_set1": {}, "rune_set2": {}, "rune_set3": {}, "rune_set4": {}}
        rune_options = get_champion_runes(champion)
        rune_set_counter = 1
        for rune_set in rune_options:  # Iterar sobre las 4 opciones de sets de runas
            actual_rune_set = "rune_set" + str(rune_set_counter)
            champion_runes[champion][actual_rune_set]["primary_runes"] = rune_set[0]  # Rama principal
            champion_runes[champion][actual_rune_set]["secondary_runes"] = rune_set[1]  # Rama Secundaria
            shards = []
            for shard in range(len(rune_set[2])):
                shards.append(shard_rows[shard][rune_set[2][shard]])
            champion_runes[champion][actual_rune_set]["shards"] = shards  # Fragmentos
            rune_set_counter += 1
    with open('champions_runes.json', 'w') as fp:
        json.dump(champion_runes, fp)


generate_json_runes()
