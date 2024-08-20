import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
np.random.default_rng(seed=100)
SHOW=True

df = pd.read_csv('Data_intreview.csv', )
df['Datums.un.laiks'] = '2000.' + df['Datums.un.laiks'].astype(str)
df['Datums.un.laiks'] = pd.to_datetime(df['Datums.un.laiks'], format="%Y.%m.%d %H:%M")
# Pamatgads 1900 nav garais gads, taču datos ir 29 februāris, līdz ar to jāpieņem kāds garais gads. Diemžēl datetime nesanāca nekā sakarīgi nomainīt gadu pirms datuma nolasīšanas, līdz ar to nākas savienot divus tekstus un tad salauzt tos.
df = df.sort_values(by='Datums.un.laiks')

df.boxplot(column=["x1", "x2", "x3"])
# plt.title("Kastu grafiki trīs stacijās")
if SHOW:
    plt.show()
else:
    plt.savefig('kastes_kluda.png', dpi=150)
fig = plt.figure()

cutoff = max(max(df["x1"]),max(df["x2"]))


print("Elementi, kuri ir lielāki trešajā stacijā par lielākajām vērtībām pirmajā un otrajā:", "\n", df[df["x3"]>cutoff])
# Jāievēro, ka visi šie izlēcēji ir secīgās minūtēs vienā un tajā pašā dienā. Visticamāk, ka šī ir sensora kļūda un konkrētais laika periods ir jāignorē.

df[df["x3"]>cutoff]=np.nan           # pārvērš milzīgās vērtības par NaN


mins, maxs = np.nanargmin(np.diff(df['x1'])), np.nanargmax(np.diff(df['x1']))
# atradām lielākos izmaiņu pīķus
minimum = np.nanmin(df['x1'].iloc[maxs+1:mins])
# aprēķinām, kāda ir mazākā vērtība starp pīķiem un atņemam to
df['x1'].iloc[maxs+1:mins] = df['x1'].iloc[maxs+1:mins] - minimum

plt.plot(df["Datums.un.laiks"][:-1], np.diff(df['x1']))
if SHOW:
    plt.show()
else:
    plt.savefig('starpibas.png')

plt.plot(df["Datums.un.laiks"], df['x1'])
if SHOW:
    plt.show()
else:
    plt.savefig("x1.png")


avgs = np.empty([12,3])
avgs[:] = np.nan
for i in range(3):
    for m in range(12):
        values = df[df['Datums.un.laiks'].dt.month == m + 1].iloc[:, i+1]
        if len(values[pd.isna(values[:])]) / len(values) <= 0.2:
            avgs[m,i] = np.nanmean(values)
print("Vidējās vērtības mēnešos un stacijās:")
for i in range(12):
    print(i+1, " & ", '%.3f'%(avgs[i,0]), " & ", '%.3f'%(avgs[i, 1]), " & ", '%.3f'%(avgs[i, 2]), "\\\\")


df.boxplot(column=["x1", "x2", "x3"])
plt.gca().set_ylim([-1,17])
if SHOW:
    plt.show()
else:
    plt.savefig("kastes_labs.png")
    fig = plt.figure()

plt.boxplot(np.random.gamma(3.5, 0.8, size=len(df)))
plt.grid(visible=True, which='major')
plt.gca().set_ylim([-1,17])
if SHOW:
    plt.show()
else:
    plt.savefig('Gamma.png')


# Acīmredzami sadalījums ir tikai pozitīvs, jo apakšējā vērtība visās stacijās ir nulle. Visticamāk, ka sadalījums nav ierobežots no augšas, jo maksimālās vērtības visiem ir dažādas un augšējā aste ir vidēji gara. Tomēr vērtības nav īpaši lielas, ar 500 000 gadījumiem neviens nepārsniedz pat 20 (atskaitot atsevišķās 15 minūtes trešajā stacijā).
# Vidējā vērtība ir nedaudz virs 2, taču tā ne obligāti ir arī matemātiskā cerība.
# Varam pieņemt Gamma sadalījumu, jo tas ir ļoti vispārīgs, un bez informācijas par datiem mums nav iemesla pieņemt kaut ko konkrētāku. Piemeklējot vispirms formu, kuras IQR un vidējā vērtība ir atbilstoša pārējām stacijām, un tad meklējot mērogu, kura aste ir atbilstoša garuma, varam būt diezgan droši par atrasto sadalījumu.



