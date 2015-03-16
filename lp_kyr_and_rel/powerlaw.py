#!/usr/bin/python
import os
from xspec import *
from pylab import *
from time import time


#plot function for playing
def plot(E,V,name,log=True):
	f, ax = plt.subplots()		
	ax.plot(E,V,"r")
	ax.grid(True)
	ax.set_xlabel("Energy [keV]")
	ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
	ax.set_xscale('log')
	ax.set_yscale('log')
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles, labels,loc = "lower left")
	savefig(name+".pdf")
	show()
	
AllModels.lmod("ky","/mnt/31660B856FD2FABA/xspec/models/ky_lampostline/")
Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/ky_lampostline/")
AllModels.setEnergies(".1 50. 1000 log")

#os.remove("fakeit_epn_ff20_sdY9_v12.0_1.fak")

def opakuj(n):
	k, l = 0, 0
	for i in range(n):
		#loading model, setting parameters
		m = Model("phabs*(pow)")
		m.setPars({1:7.5e-2,2:3,3:1e-3})

		print "####################################"
		print AllModels.eqwidth("3")
		print "####################################"
		AllModels.show()

		#using fakeit function to generate data
		fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=1e6)
		AllData.fakeit(1,fs,True,"fakeit_")
		AllModels.setEnergies(".1 10. 1000 log")
		AllData.ignore("**-0.1 10.0-**")
		AllData.show()

		#redefining model for fitting

		AllModels.show()
		Fit.nIterations = 100000
		Fit.perform()

		#Fit.steppar("11 -10 -2 10 12 3 20 10")

		Plot.setRebin("100","200")
		Plot.xAxis = "keV"
		Plot.device = "/xs"
		#Plot("contour")
		
		Plot("ldata","emodel","ratio", "residuals")


		#x = Plot.x()
		#y = Plot.y()
		#plot(x,y,"multiple")
		"""
		f = open('myfilekyr.txt','a')
		f.write(str(m(10).values[0])+" "+str(m(11).values[0])+" "+str(m(12).values[0])+"\n") 
		f.close()
		if m(10).values[0] > -3:
			if k == 0:
				x_min = x[:]
				y_min = y[:]
				k += 1
				q_min = m(10).values[0]
			else: pass
		if m(10).values[0] < -9.9:
			if l == 0:
				x_max = x[:]
				y_max = y[:]
				l += 1
				q_max = m(10).values[0]
			else: pass
		print k,l
		if k == 1 and l == 1: 
			return x_min, y_min, x_max, y_max, q_min, q_max
		"""
opakuj(1)

"""
x_min, y_min, x_max, y_max, q_min, q_max = opakuj(10)

f, ax = plt.subplots()		
ax.plot(x_min, y_min,"r", label="q_out"+str(q_min))
ax.plot(x_max, y_max,"b", label="q_out"+str(q_max))
ax.grid(True)
ax.set_xlabel("Energy [keV]")
ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
#ax.set_xscale('log')
ax.set_yscale('log')
ax.set_title("kyrline")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels,loc = "lower left")
savefig("multiplekyr.pdf")
show()
"""