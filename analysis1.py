from read_profiles import vert_profs
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from read_modules import goes

p = 'CHC'
a = vert_profs(p)
g = goes(p)

print(len(g.CTH.data))
print(len(g.CTH.times))

x,y = np.meshgrid(a.altitudes, a.times)

fig, ax = plt.subplots()
im = ax.contourf(y.T, x.T, a.data.T)
ax.plot(g.CTH.times,g.CTH.data, lw = 2, c = 'r')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H:00'))
fig.colorbar(im)
plt.show()

