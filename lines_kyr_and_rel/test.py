from xspec import *
from pylab import *

Xset.addModelString("RELLINE_TABLES","/home/mecgyver/xspec/relline/")
AllModels.lmod("relline","/home/mecgyver/xspec/relline/")
AllModels.setEnergies(".1 50. 1000 log")

m1 = Model("relline")

x1=m1.energies(0)
y1=m1.values(0)
x1.pop()


f, ax = plt.subplots()
ax.plot(x1,y1, "r")
ax.grid(True)
ax.set_title('Relline')
ax.set_xlabel("Energy [keV]")
ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
ax.set_xscale('log')
ax.set_yscale('log')
savefig("relline.pdf")
