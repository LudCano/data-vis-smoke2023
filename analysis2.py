from read_profiles import vert_profs
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from read_modules import goes
import datetime as dt

plt.rc('font', size = 15)

p = 'Airport'
ps = ['LFA','Airport','Ancohuma','CHC']
alts = [3700,3818,3956,3704]


fig, ax = plt.subplots(4,1, sharex = True)

axi = 0
for i, j in zip(ps, alts):
    a = vert_profs(i)
    g = goes(i)
    x,y = np.meshgrid(a.altitudes, a.times)
    im = ax[axi].contourf(y.T, x.T, a.data.T, cmap = 'jet')
    ax2 = ax[axi].twinx()
    ax2.scatter(g.AOD.times, g.AOD.data, s = 6, c = 'k', marker = 's', label = 'AOD')
    ax[axi].axhline(j, ls='--',c='k')
    #ax[axi].legend()
    ax[axi].set_ylim(3600,16000)
    ax[axi].set_xlim(a.times[0], dt.datetime(2023,10,29,15))
    ax[axi].set_ylabel(i)
    axi = axi + 1

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(im, cax=cbar_ax, label = 'RH[%]')
#ax.set_xlabel('Local Time')
#ax[-1].set_ylabel('Altitude [m]')
ax[-1].xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
#fig.colorbar(im, label = 'RH [\%]')
plt.show()

