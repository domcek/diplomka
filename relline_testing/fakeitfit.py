#!/usr/bin/python
from xspec import *
from pylab import *

AllModels.lmod("ky","/mnt/31660B856FD2FABA/xspec/models/ky_lampostline/")
Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/ky_lampostline/")
AllModels.lmod("relline","/mnt/31660B856FD2FABA/xspec/models/relline/")
AllModels.setEnergies(".1 50. 1000 log")


n=1

for i in range(n):
	m = Model("phabs*(pow+relline)")
	m.setPars({1:9.22e-3,2:2,3:1.5e-2,5:2.95,6:2.95,8:0.91,9:33,14:4e-4}) ###parameters

	print "####################################"
	print AllModels.eqwidth("3")
	print "####################################"
	AllModels.show()

	fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=1e6)
	AllData.fakeit(1,fs,True,"fakeit_")
	AllModels.setEnergies(".1 10. 1000 log")
	AllData.ignore("**-0.1 10.0-**")
	AllData.show()
	
	m2 = Model("phabs*(pow+relline_lp)")
	m2(12).link = "2"
	m2(7).frozen = False
	m2(4).frozen = True
	Fit.nIterations = 100000
	Fit.perform()
	f = open('rel.txt','a')
	f.write(str(m2(5).values[0])+"\n") 
	f.close()
	"""
	m3 = Model("phabs*(pow+kyrline)")
	m3.setPars({1:9.22e-3,13:0})
	m3(14).link = "2"
	m3(11).frozen = False
	m3(10).frozen = True
	m3(12).frozen = False
	m3(1).frozen = True

	Fit.nIterations = 100000
	Fit.perform()
	m3(10).frozen = False
	Fit.nIterations = 100000
	Fit.perform()

	AllModels.eqwidth("3")
	f = open('kyr.txt','a')
	f.write(str(m3(10).values[0])+"\n") 
	f.close()
	

	Plot.setRebin("5","10")
	Plot.xAxis = "keV"
	Plot.device = "/xs"
	Plot("ldata","emodel","ratio", "residuals")
	"""	
