#!/usr/bin/python
from xspec import *
from pylab import *
import numpy as np

#AllModels.initpackage("kyreflionx", "lmodel.dat" ,"/mnt/31660B856FD2FABA/xspec/models/kyreflionx/ -udmget64")
AllModels.lmod("ky","/mnt/31660B856FD2FABA/xspec/models/ky_lampostline/")
Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/ky_lampostline/")
AllModels.setEnergies(".1 50. 1000 log")


m = Model("kyrline")
m.setPars({(1):0.7})

fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=2e5)
AllData.fakeit(1,fs,True,"fakeit_")
AllModels.setEnergies(".1 10. 1000 log")
AllData.ignore("**-3.0 10.0-**")
AllData.show()

n=25
out = 7
step1 = 0.08
#step2 is calculated so that outer boundry is 400 rg
def create_r(n,out,step1):
	r=[]
	
	start = 1.1
	end = start+(n-out)*step1
	b = np.arange(start,end,step1)
	step2 = (6-b[-1]-step1)/out
	c = np.arange(b[-1]+step1, 6+step2, step2)
	b = np.append(b, c)

	for i in range(n):
		k = [np.exp(b[i]),np.exp(b[i+1])]
		r.append(k)
	return r

r = create_r(n,out,step1)
print r


# for surface rings normalization
S = []
for i in range(len(r)):
	Sm = np.pi*(r[i][1]-r[i][0])
	S.append(Sm)

if n == 5:
	m = Model("kyrline+kyrline+kyrline+kyrline+kyrline")

if n == 10:
	m = Model("kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline")

if n == 25:
	m = Model("kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline+kyrline")

for i in range(n):
	m(1+i*13).frozen = True
	m(2+i*13).frozen = True
	m.setPars({(1+i*13):0.7})

	print i
	rin = 3+i*13
	rout = 5+i*13
	print rin, r[i][0]
	print rout, r[i][1]
	m.setPars({rin:r[i][0],rout:r[i][1]})

AllModels.show()

Fit.nIterations = 100000
Fit.perform()



val = []
valS = []
value = []
error = []
for i in range(n):
	val.append(m(13+i*13).values)
	valS.append(m(13+i*13).values[0]/S[i])
	error.append(m(13+i*13).values[1])
	value.append(m(13+i*13).values[0])

x=[]
for i in range(len(val)):
	x.append((r[i][0]+r[i][1])/2)

"""		
plot(x,value,".")
xlabel("rg")
ylabel("N(r)")
xscale('log')
yscale('log')
errorbar(x ,value, yerr = error, marker = "None", linestyle = "None") #weird stuff
grid(True)
savefig("ky_spin0.94_log.pdf")
"""
	
plot(x,valS,".")
xlabel("rg")
ylabel("N(r)")
xscale('log')
yscale('log')
#errorbar(x ,value, yerr = error, marker = "None", linestyle = "None") #weird stuff
grid(True)
savefig("ky_surfnorm_spin0.7_log.pdf")
show()
