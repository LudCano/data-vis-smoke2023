import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
pth = '0_Data\\3_SATELLITE_data\\1_GOES\\Humedad_perfil_vertical\\Airport_stations.csv'

d = pd.read_csv(pth, skiprows=7)
d.time_start = pd.to_datetime(d.time_start)
times = d.time_start
d = d.sort_values('time_start')
numdates = mdates.date2num(d.time_start)
print(numdates)
d = d.iloc[:,2:]
d.dropna(axis = 1, inplace=True)
pressures = [float(i) for i in d.columns]

a = d.to_numpy(dtype=float)

'''
y, _ = a.shape
x, y = np.meshgrid(np.arange(y), pressures)
fig, ax = plt.subplots()
cmesh = ax.pcolormesh(x,y,a.T, cmap = 'jet')
ax.invert_yaxis()
#ax.pcolormesh(a.T)
fig.colorbar(cmesh)


fig, ax = plt.subplots()
ax.scatter(a.T[:,650], pressures)
ax.invert_yaxis()

fig, ax = plt.subplots()
ax.scatter(a.T[:,583], pressures)
ax.invert_yaxis()



y_, _ = a.shape
x, y = np.meshgrid(np.arange(y_), pressures)
xx, yy = np.meshgrid(np.arange(y_), pressure_to_altitude(np.array(pressures)))
fig, ax = plt.subplots()
#cmesh = ax.pcolormesh(x,y,a.T, cmap = 'jet')
ax2 = ax.twinx()
cmesh = ax2.pcolormesh(xx,yy,a.T, cmap = 'jet')
#ax.plot(np.arange(o), turnoffs, 'k')
ax2.plot(np.arange(o), pressure_to_altitude(np.array(turnoffs)), 'k')
ax.invert_yaxis()
#ax.pcolormesh(a.T)
fig.colorbar(cmesh)

'''


sens = 1e-2
def find_turnoff(prof):
    v = a[prof,:]
    for i in range(len(v)-1):
        r = abs(v[i]-v[i+1])
        if r < sens:
            idx = pressures[i+1]
        else:
            break
    return idx

o, _ = a.shape
turnoffs = []
for j in range(o):
    try:
        turnoffs.append(find_turnoff(j))
    except:
        turnoffs.append(np.nan)


def pressure_to_altitude(pressure):
    h = (1-((pressure/1013.25)**0.190284))*145366.45*0.3048
    return h

def alt_to_press(altitude):
    p = (((1- altitude/(145366.45*0.3048)))**(1/0.190284))*1013.25
    return p



y_, _ = a.shape
#x, y = np.meshgrid(np.arange(y_), pressures)
x, y = np.meshgrid(numdates, pressures)
fig, ax = plt.subplots(figsize = (10,6),layout = 'constrained')
cmesh = ax.pcolormesh(x,y,a.T, cmap = 'jet')
ax.set_ylim(60,1000)
ax2 = ax.secondary_yaxis('right', functions = (pressure_to_altitude, alt_to_press))
ax2.set_ylabel('Altitude [m]')
ax.set_ylabel('Pressure [mbar]')
ax.scatter(numdates, turnoffs, c='k')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d%b'))
ax.invert_yaxis()
#ax.pcolormesh(a.T)
#fig.colorbar(cmesh)



plt.figure()
altitudes = pressure_to_altitude(np.array(turnoffs))
print(np.nanmean(altitudes), np.nanmedian(altitudes))
plt.hist(altitudes)
plt.show()
