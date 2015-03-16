#!/usr/bin/python
from xspec import *
from pylab import *

AllModels.lmod("ky","/mnt/31660B856FD2FABA/xspec/models/KY/")
Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/KY/")
AllModels.lmod("relline","/mnt/31660B856FD2FABA/xspec/models/relline/")
AllModels.setEnergies(".1 50. 1000 log")


n = 5
for i in range(n):
	m = Model("phabs*(pow+relline_lp)")
	h = 100
	m.setPars({1:9.22e-3,2:2,3:1.5e-2,4:6.4,5:h,6:0.91,7:33,12:2,13:4e-4}) ###parameter h = m(5)

	print "####################################"
	print AllModels.eqwidth("3")
	print "####################################"
	AllModels.show()

	fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=1e6)
	AllData.fakeit(1,fs,True,"fakeit_")
	AllModels.setEnergies(".1 10. 1000 log")
	AllData.ignore("**-0.1 10.0-**")
	AllData.show()
	
	
	m2 = Model("phabs*(pow+relline)")
	m2(7).frozen = False
	m2(5).frozen = False
	m2(6).frozen = False
	Fit.nIterations = 100000
	Fit.perform()

	f = open('rel_inverse.txt','a')
	f.write("h: "+str(h)+4*" "+str(m2(5).values[0])+4*" "+str(m2(6).values[0])+4*" "+str(m2(7).values[0])+"\n") 
	f.close()

	"""

	m3 = Model("phabs*(pow+kyrline)")
	m3.setPars({1:9.22e-3,14:0})
	m3(10).frozen = False
	m3(11).frozen = False
	m3(12).frozen = False
	Fit.nIterations = 100000
	Fit.perform()

	AllModels.eqwidth("3")
	f = open('kyr_inverse_.txt','a')
	f.write("h: "+str(h)+4*" "+str(m3(10).values[0])+4*" "+str(m3(11).values[0])+4*" "+str(m3(12).values[0])+"\n") 
	f.close()
	
	
	Plot.setRebin("5","10")
	Plot.xAxis = "keV"
	Plot.device = "/xs"
	Plot("ldata","emodel","ratio", "residuals")
	"""	
