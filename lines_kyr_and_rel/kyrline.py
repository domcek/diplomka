#!/usr/bin/python
from xspec import *
from pylab import *

def plotting(x,y,n,nazov):
	f, ax = plt.subplots()
	for i in range(n):
		ax.plot(x[i],y[i])
		handles, labels = ax.get_legend_handles_labels()
		ax.legend(handles, labels,loc = "lower left")
	ax.grid(True)
	ax.set_xlabel("Energy [keV]")
	ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
	ax.set_xscale('log')
	ax.set_yscale('log')
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles, labels,loc = "lower left")
	savefig("kyrline_"+str(nazov)+".pdf")
	
def basic_plot(x,y,nazov):
	f, ax = plt.subplots()
	ax.plot(xpl,ypl)
	ax.grid(True)
	ax.set_xlabel("Energy [keV]")
	ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
	ax.set_xscale('log')
	ax.set_yscale('log')
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles, labels,loc = "lower left")
	savefig("kyrline_"+nazov+".pdf")


#AllModels.initpackage("ky", "lmodel.dat" ,"/mnt/31660B856FD2FABA/xspec/models/KY/")
AllModels.lmod("ky","/mnt/31660B856FD2FABA/xspec/models/KY/")
Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/KY/")

# Create an array of 1000 logarithmic-spaced bins, from .1 to 50. keV
AllModels.setEnergies(".1 10. 10000 log")

"""
m = Model("kyrline")
x=m.energies(0)
y=m.values(0)
m.setPars({1:i})

#m.energies(0) - Returns a list of energy array elements, 
#the size will be 1 larger than the corresponding flux array, not sure why
x.pop()
"""
x=[]
y=[]
spin = [0,0.7,1]
for a in spin:
	m = Model("kyrline")
	m.setPars({1:a})
	xz=m.energies(0)
	yz=m.values(0)
	xz.pop()
	x.append(xz)
	y.append(yz)

plotting(x,y,len(spin),"sp")

x=[]
y=[]
inkl = [30,60,85]
for i in inkl:
	m = Model("kyrline")
	m.setPars({2:i})
	xz=m.energies(0)
	yz=m.values(0)
	xz.pop()
	x.append(xz)
	y.append(yz)
	
plotting(x,y,len(inkl),"inklinacia")

x=[]
y=[]
emis = [2,3,5]
for e in emis:
	m = Model("kyrline")
	m.setPars({7:e})
	xz=m.energies(0)
	yz=m.values(0)
	xz.pop()
	x.append(xz)
	y.append(yz)
	
plotting(x,y,len(inkl),"emisivita")

m = Model("kyrline")
m.setPars({1:1,2:30})
xz=m.energies(0)
yz=m.values(0)
xz.pop()
xpl=xz
ypl=yz

basic_plot(xpl,ypl,"nazov")


f, ax = plt.subplots()
ax.plot(xpl,ypl)
ax.grid(True)
ax.set_xlabel("Energy [keV]")
ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
ax.set_xscale('log')
ax.set_yscale('log')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels,loc = "lower left")
savefig("kyrline_pl.pdf")





