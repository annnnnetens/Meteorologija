import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime, timedelta
import xarray as xr
SHOW=True

loc = "ECMWF_prognozes.nc"
xrds = xr.open_dataset(loc)


dates = [datetime.fromisoformat('2022-07-05T22:00:00.000000000'), datetime.fromisoformat('2022-07-06T12:00:00.000000000'), datetime.fromisoformat('2022-07-06T19:00:00.000000000')]
# datumi un laiki ir Griničas laikā, līdz ar to Latvijai ir jāskatās trīs stundas agrāk.
defaulttime = datetime.fromisoformat('2022-07-05T21:00:00.000000000')

zerodata = xrds.sel(time=defaulttime)
data_1 = xrds.sel(time=dates[0])
data_15 = xrds.sel(time=dates[1])
data_22 = xrds.sel(time=dates[2])


minim = np.array(data_1['ssr'].data-zerodata['ssr'].data).min()
maxim = np.array(data_22['ssr'].data-zerodata['ssr'].data).max()

fig, axs = plt.subplots(nrows=1,ncols=3)
f = 1.0/np.cos(np.mean(data_22['latitude'])*np.pi/180)
# koordināšu proporcija, lai projekcija atbilstu kartes vidum
for i in range(3):
    axs[i].set_aspect(f)
    axs[i].set_xticks([])
    axs[i].set_yticks([])
    axs[i].set_title((dates[i]+timedelta(hours=3)).strftime("%X"))

cs0 = axs[0].contourf(data_1['longitude'], data_1['latitude'], data_1['ssr']-zerodata['ssr'], vmin=minim, vmax=maxim)
cs1 = axs[1].contourf(data_15['longitude'], data_15['latitude'], data_15['ssr']-zerodata['ssr'], vmin=minim, vmax=maxim)
cs2 = axs[2].contourf(data_22['longitude'], data_22['latitude'], data_22['ssr']-zerodata['ssr'], vmin=minim, vmax=maxim)

fig.subplots_adjust(top=0.8)
cbar_ax = fig.add_axes([0.15, 0.2, 0.7, 0.05])
fig.colorbar(cs2, cax=cbar_ax, orientation='horizontal', aspect=30, extend={'both'})
if SHOW:
    plt.show()
else:
    plt.savefig("baltija.png")


liepaja = xrds.sel(longitude=21.0, latitude=56.3)
aluksne = xrds.sel(longitude=27.3, latitude=57.3)
dagda = xrds.sel(longitude=27.3, latitude=56.5)

datumi = liepaja['time'][:-1]
fig = plt.plot()
plt.plot(datumi, np.diff(liepaja['ssr'])/3600, label='Liepāja')
plt.plot(datumi, np.diff(aluksne['ssr'])/3600, label='Alūksne')
plt.plot(datumi, np.diff(dagda['ssr'])/3600, label='Dagda')
plt.ylabel('W/m^2')
plt.legend()
# plt.title("Stundas vidējās radiācijas vērtības Latvijas pilsētās")
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
if SHOW:
    plt.show()
else:
    plt.savefig("pilsetas.png")