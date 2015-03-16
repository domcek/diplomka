#!/usr/bin/python
from xspec import *
from pylab import *

def plotting(x,y,x2,y2,i,value):
	f, ax = plt.subplots()		
	ax.plot(xkyrsp[i],ykyrsp[i],"r")
	ax.plot(xrelsp[i],yrelsp[i],"b")
	ax.grid(True)
	ax.set_xlabel("Energy [keV]")
	ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
	ax.set_xscale('log')
	ax.set_yscale('log')
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles, labels,loc = "lower left")
	savefig("kyrvsrel_spin_"+str(value)+".pdf")
	
def plotting2(x,y,x2,y2,i,value):
	f, ax = plt.subplots()		
	ax.plot(xkyrangle[i],ykyrangle[i],"r")
	ax.plot(xrelangle[i],yrelangle[i],"b")
	ax.grid(True)
	ax.set_xlabel("Energy [keV]")
	ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
	ax.set_xscale('log')
	ax.set_yscale('log')
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles, labels,loc = "lower left")
	savefig("kyrvsrel_inclination_"+str(value)+".pdf")
	
def energies(lst):
	energy= []
	for i in range(1,len(lst)):
		energy.append((float(lst[i])+float(lst[i-1]))/2)
	return energy
	

	
#AllModels.initpackage("ky", "lmodel.dat" ,"/mnt/31660B856FD2FABA/xspec/models/ky_lampostline/")
	
AllModels.lmod("relxill","/mnt/31660B856FD2FABA/xspec/models/relxill/")
AllModels.lmod("ky","/mnt/31660B856FD2FABA/xspec/models/ky_lampostline/")
Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/ky_lampostline/")

# Create an array of 1000 logarithmic-spaced bins, from .1 to 50. keV
AllModels.setEnergies(".1 50. 1000 log")


##spin for kyrline
sp = [0.0,0.7,0.98]
xkyrsp=[]
ykyrsp=[]
for s in sp:
	m = Model("kyrline")
	m.setPars({1:s,10:0})
	xz=m.energies(0)
	print len(xz)
	yz=m.values(0)
	xz = energies(xz)
	xkyrsp.append(xz)
	ykyrsp.append(yz)
	print len(xz), len(yz)	

#spin for relline	
xrelsp=[]
yrelsp=[]
for s in sp:
	m = Model("relline_lp")
	m.setPars({3:s,2:3})
	xz=m.energies(0)
	yz=m.values(0)
	xz = energies(xz)
	xrelsp.append(xz)
	yrelsp.append(yz)

#angle
ang = [30.0,60.0,85.0]
xkyrangle=[]
ykyrangle=[]
for s in ang:
	m = Model("kyrline")
	m.setPars({1:0.7,2:s,10:0.0})
	xz=m.energies(0)
	yz=m.values(0)
	xz = energies(xz)
	xkyrangle.append(xz)
	ykyrangle.append(yz)

#spin for relline	
xrelangle=[]
yrelangle=[]
for s in ang:
	m = Model("relline_lp")
	m.setPars({2:3.0,3:0.7,4:s})
	xz=m.energies(0)
	yz=m.values(0)
	xz = energies(xz)
	xrelangle.append(xz)
	yrelangle.append(yz)
	


#for name used spin value
for i in range(3):
	plotting(xkyrsp[i],ykyrsp[i],xrelsp[i],yrelsp[i],i,sp[i])	
	plotting2(xkyrangle[i],ykyrangle[i],xrelangle[i],yrelangle[i],i,ang[i])	
"""
f, ax = plt.subplots()		
ax.plot(xkyr[2],ykyr[2])
ax.plot(xrel[2],yrel[2])
ax.grid(True)
ax.set_xlabel("Energy [keV]")
ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
ax.set_xscale('log')
ax.set_yscale('log')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels,loc = "lower left")
savefig("kyrvsrel_spin_"+"test"+".pdf")
"""
