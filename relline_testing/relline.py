#!/usr/bin/python
from xspec import *
from pylab import *

AllModels.lmod("relline","/mnt/31660B856FD2FABA/xspec/models/relline/")
AllModels.setEnergies(".1 50. 1000 log")


for i in range(20):
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