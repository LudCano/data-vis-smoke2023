from read_modules import goes
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ancohuma = goes('Ancohuma')
#print(ancohuma.show_vars())
tpw = [float(i) for i in ancohuma.TPW.data]
tt = [float(i) for i in ancohuma.TT.data]
#pa que ya no tengas que escribir cada rato ancohuma.CTH
cth = ancohuma.CTH.data
#print(cth.full_name)
cod = ancohuma.COD.data

tiempos = ancohuma.TPW.datenum

fig, ax = plt.subplots()
ax.scatter(tiempos, tpw)
ax2 = ax.twinx()
ax2.plot(tiempos, tt, c='r')
ax2.set_ylabel(ancohuma.TT.units)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
ax.set_title(ancohuma.TPW.full_name)
ax.set_ylabel(ancohuma.TPW.units)



###TT VS TPW

#fig, ax = plt.subplots()
#ax. scatter(tt, tpw)
#ax.set_title("TT VS TPW FIGHT")
#ax.set_xlabel(ancohuma.TT.units)
#ax.set_ylabel(ancohuma.TPW.units)
#plt.show()

print(len(cod))
print(len(cth))

#COD VS CTH
fig, ax = plt.subplots()
c = ax.scatter(cod, cth,c = ancohuma.COD.datenum, cmap = 'viridis', alpha = .3)
ax.set_title("COD VS CTH FIGHT")
ax.set_xlabel(ancohuma.COD.units)
#ax.set_xscale('log')
fig.colorbar(c)
ax.grid()
ax.set_ylabel(ancohuma.CTH.units)
plt.show()

