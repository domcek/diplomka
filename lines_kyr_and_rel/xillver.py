#!/usr/bin/python
from xspec import *
from pylab import *

def plotting(x,y,n):
	f, ax = plt.subplots()
	for i in range(n):
		ax.plot(x[i],y[i])
	ax.grid(True)
	ax.set_xlabel("Energy [keV]")
	ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
	ax.set_xscale('log')
	ax.set_yscale('log')
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles, labels,loc = "lower left")
	savefig("xillver.pdf")	


AllModels.lmod("relxill","/mnt/31660B856FD2FABA/xspec/models/relxill/")
#sucast relxill

# Create an array of 1000 logarithmic-spaced bins, from .1 to 50. keV
AllModels.setEnergies(".1 50. 1000 log")
n=3
x=[]
y=[]
for i in range(n):
	m = Model("xillver")
	m.setPars({5:i})
	Plot.device = "/xs"
	Plot("m")
	xz=m.energies(0)
	yz=m.values(0)
	xz.pop()
	x.append(xz)
	y.append(yz)


plotting(x,y,n)




#m.energies(0) - Returns a list of energy array elements, 
#the size will be 1 larger than the corresponding flux array, not sure why


"""
f, ax = plt.subplots()
ax.plot(x,y)
ax.plot(x2,y2)
ax.grid(True)
ax.set_xlabel("Energy [keV]")
ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
ax.set_xscale('log')
ax.set_yscale('log')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels,loc = "lower left")
savefig("xillver.pdf")	
"""
