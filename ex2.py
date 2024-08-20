import pandas as pd
import csv
import os.path
import glob
from urllib.request import urlretrieve
from collections import Counter
import matplotlib.pyplot as plt
import geopandas as gpd
import pycountry
SHOW=True

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


cb = gpd.read_file('ne_110m_admin_0_countries')
cb = cb.assign(MESSAGES=0)

if True:
    c = Counter()
    valstis = Counter()
    empty_messages = set()
    nezinamas_valstis = set()
    friends = ESWI[ESWI["Receivers"].apply(lambda x: 'UMRR' in x)]
    # apakštabula, kur adresāti iekļauj UMRR
    for CC in friends["CCCC"]:
        if (Vol["CCCC"] == CC).any():
            names = Vol[Vol["CCCC"] == CC].iloc[0,2]
            # nosaukums valstij, kuras CCCC tiek apskatīts
            if pycountry.countries.get(name=names):
                valstis[pycountry.countries.get(name=names).alpha_3] += 1
            elif pycountry.countries.get(official_name=names):
                valstis[pycountry.countries.get(official_name=names).alpha_3] += 1
            else:
                nezinamas_valstis.add(names)
            c[names]+= 1
        else:
            empty_messages.add(CC)
    print("Nezināmie: ", nezinamas_valstis)
    print("CCCC bez attiecīgas valsts: ", empty_messages)
    print("USA" in valstis)
    print(cb[cb['SOV_A3']=='USA'])
    # for el in c.most_common():
    #     print(f"\item[{el[1]}] {el[0]}")
    for valsts in valstis:
        cb.loc[cb['ADM0_A3']==valsts, 'MESSAGES'] = valstis[valsts]


cb.plot(column='MESSAGES', legend=True)
if SHOW:
    plt.show()
else:
    plt.savefig("pasaule.png")


if True:
    for _, row in Vol.iterrows():
        folder = f"./data/{row['Region']}/{row['RTH']}/{row['Country']}/{row['CCCC']}/"
        if not os.path.exists(folder):
            os.makedirs(folder)
        name = f"{row['Country']}_{row['TTAAii']}_{row['CCCC']}_{row['TimeGroup']}.txt"
        row.to_csv(os.path.join(folder, name) , index=False, header=False, quoting=csv.QUOTE_ALL)

    nosaukumi = ['UMRR', 'ESWI', 'EEMH']
    for cc in nosaukumi:
        print(f"Mape {cc}:")
        # zinām, cik apakšmapēs mums ir jāskatās
        faili = glob.glob(f"./data/*/*/*/{cc}/*")
        for fails in faili:
            print(os.path.relpath(fails))


