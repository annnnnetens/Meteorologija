import pandas as pd
import csv
import os.path
import glob
from urllib.request import urlretrieve
from collections import Counter
import matplotlib.pyplot as plt
import geopandas as gpd
# import geodatasets
# import plotly.express as px
# import pycountry


Vol_URL = 'https://wis.wmo.int/operational-info/VolumeC1/VolC1.txt'
ESWI_URL = 'https://wis.wmo.int/operational-info/GTS_routeing/ESWI/ESWIroca.txt'



Vol = pd.read_csv(Vol_URL, quoting=csv.QUOTE_ALL, quotechar='"', encoding='latin-1')
# tā kā šī ir smuka tabula, tad visu apstrādi var veikt pa taisno ar pandām.

if os.path.isfile('ESWIroca.txt'):
    ESWI = pd.read_csv('ESWIroca.txt')
else:
    f = open(urlretrieve(ESWI_URL)[0])
    ESWI = pd.DataFrame(columns=['TTAAii', 'CCCC', 'Receivers'])
                    # otrs fails nav tabula, līdz ar to nāksies to iterēt.
    f.readline()    # pirmā rinda nav vajadzīga, tādēļ to jānolasa.
    for line in f:
        objs = line[:-1].split(',')                     # sadala visu pa komatiem, noņem \n
        objs = [item.strip('\"') for item in objs]      # noņem pēdiņas
        sender = objs[0].split()                        # sadala pirmo vārdu divos
        ESWI = pd.concat([ESWI, pd.DataFrame([[sender[0], sender[1], objs[1:]]], columns=ESWI.columns)], ignore_index=True)
    ESWI.to_csv('ESWIroca.txt', index=False)            # saglabā, lai nebūtu tas vēlreiz jādara



if False:
    c = Counter()
    empty_messages = set()
    friends = ESWI[ESWI["Receivers"].apply(lambda x: 'UMRR' in x)]
    for CC in friends["CCCC"]:
        if (Vol["CCCC"] == CC).any():
            names = Vol[Vol["CCCC"] == CC].iloc[0,2]
            # possibles = pycountry.countries.search_fuzzy(names)
            # print(possibles)
            # print(pycountry.subdivisions.search_fuzzy(names))
            # # possibles.append(pycountry.subdivisions.search_fuzzy(names))
            # print(possibles)
            # country = possibles[0].alpha_3
            c[names]+= 1
            # TODO: valstis nestrādā.
        else:
            empty_messages.add(CC)
    # print(c)
    # print("Šie CCC netika atrasti: \n", empty_messages)
    print(c.most_common()[:-30])

country_boundaries = gpd.read_file('ne_110m_admin_0_countries')
country_boundaries.plot()
plt.show()

# fig = plt.figure(figsize=(20, 10))
# ax = fig.add_subplot()
# country_boundaries.plot(
#     ax=ax,
#     cmap="Pastel1",
#     edgecolor="black",
#     alpha=0.5
# )

if False:
    for _, row in Vol.iterrows():
        folder = f"./data/{row['Region']}/{row['RTH']}/{row['Country']}/{row['CCCC']}/"
        if not os.path.exists(folder):
            os.makedirs(folder)
        name = f"{row['Country']}_{row['TTAAii']}_{row['CCCC']}_{row['TimeGroup']}.txt"
        row.to_csv(os.path.join(folder, name) , index=False, header=False, quoting=csv.QUOTE_ALL)

# homepath = '/Users/anete/Documents/Meteorologija/'

nosaukumi = ['UMRR', 'ESWI', 'EEMH']
for cc in nosaukumi:
    print(f"Mape {cc}:")
    # zinām, cik apakšmapēs mums ir jāskatās
    faili = glob.glob(f"/Users/anete/Documents/Meteorologija/data/*/*/*/{cc}/*")
    for fails in faili:
        print(os.path.relpath(fails))


