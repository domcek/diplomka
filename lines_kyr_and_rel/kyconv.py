#!/usr/bin/python
from xspec import *
from pylab import *


AllModels.lmod("ky","/mnt/31660B856FD2FABA/xspec/models/KY/")
Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/KY/")

AllModels.setEnergies(".1 50. 1000 log")

m1 = Model("kyconv*pexmon")

x1=m1.energies(0)
y1=m1.values(0)
x1.pop()


f, ax = plt.subplots()
ax.plot(x1,y1, "r")
ax.plot(x2,y2, "g")
ax.grid(True)
ax.set_title('kyconv*pexmon + pexmon')
ax.set_xlabel("Energy [keV]")
ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
ax.set_xscale('log')
ax.set_yscale('log')
savefig("kyconv.pdf")

