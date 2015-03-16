#!/usr/bin/python
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
	
AllModels.lmod("relline","/mnt/31660B856FD2FABA/xspec/models/relline/")
AllModels.setEnergies(".1 50. 1000 log")

def opakuj(n):
	k, l = 0, 0
	for i in range(n):
		#loading relliine_lp model, setting parameters
		m = Model("phabs*(pow+relline_lp)")
		#m.setPars({1:7.5e-2,2:3,3:1e-3,5:3,7:60,13:3e-6}) hodnoty pre 1H
		m.setPars({1:9.22e-3,2:2,3:1.5e-2,5:3,6:0.91,7:33,13:4e-4})
		m(12).link = "2"
		AllModels.eqwidth("3")
		AllModels.show()


		#using fakeit function to generate data
		fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=1e6)
		AllData.fakeit(1,fs,True,"fakeit_")
		AllModels.setEnergies(".1 10. 1000 log")
		AllData.ignore("**-0.1 10.0-**")
		AllData.show()
		V = AllData(1).values
		E = AllData(1).energies

		#creating second fitting model relline
		m2 = Model("phabs*(pow+relline)")
		m2.setPars({5:"3 0.1 0 0 10 10"})
		m2(5).frozen = False
		m2(7).frozen = False
		m2(9).frozen = False
		AllModels.show()
		Fit.nIterations = 10000
		Fit.perform()

		f = open('index1.txt','a')
		f.write(str(m2(5).values[0])+"\n") 
		f.close()

		Plot.setRebin("5","10")
		Plot.xAxis = "keV"
		#Plot.device = "/xs"
		#Plot("ldata","emodel","ratio", "residuals")
		#Plot("emodel")

		#x = Plot.x()
		#y = Plot.y()
		"""
		f = open('myfile.txt','a')
		f.write(str(m2(5).values[0])+" "+str(m2(6).values[0])+" "+str(m2(7).values[0])+"\n") 
		f.close()
		if m2(6).values[0] > 9:
			if k == 0:
				x_min = x[:]
				y_min = y[:]
				q_min = m2(6).values[0]
				k += 1
			else: pass
		if m2(6).values[0] < 3:
			if l == 0:
				x_max = x[:]
				y_max = y[:]
				q_max = m2(6).values[0]
				l += 1
			else: pass
		print k,l
		if k == 1 and l == 1: 
			return x_min, y_min, x_max, y_max, q_min, q_max
		"""
opakuj(10)

"""
x_min, y_min, x_max, y_max, q_min, q_max = opakuj(10)

f, ax = plt.subplots()	
ax.plot(x_max, y_max,"r", label="q_out"+str(q_max))	
ax.plot(x_min, y_min,"b", label="q_out"+str(q_min))
ax.grid(True)
ax.set_xlabel("Energy [keV]")
ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
#ax.set_xscale('log')
ax.set_yscale('log')
ax.set_title("relline")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels,loc = "lower left")
savefig("multiplerel.pdf")
show()
"""