#!/usr/bin/python
from xspec import *
from pylab import *
import numpy as np

def create_r(n,out,step1):
	r=[]
	
	start = 1.2
	end = start+(n-out)*step1
	b = np.arange(start,end,step1)
	step2 = (6-b[-1]-step1)/out
	c = np.arange(b[-1]+step1, 6+step2, step2)
	b = np.append(b, c)

	for i in range(n):
		k = [np.exp(b[i]),np.exp(b[i+1])]
		r.append(k)
	return r

def create_mo(n):
	string = "kyreflionx+"
	new_string = ""
	for i in range(n):
		new_string += string 
		if i == (n-1):
			new_string = new_string[:-1] 
	return new_string

#AllModels.initpackage("kyreflionx", "lmodel.dat" ,"/mnt/31660B856FD2FABA/xspec/models/kyreflionx/ -udmget64")
AllModels.lmod("kyreflionx","/mnt/31660B856FD2FABA/xspec/models/kyreflionx/")
Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/kyreflionx/")
AllModels.setEnergies(".1 50. 1000 log")


m = Model("kyreflionx")
spin = 0.7
m.setPars({1:spin})

fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=2e5)
AllData.fakeit(1,fs,True,"fakeit_")
AllModels.setEnergies(".1 10. 1000 log")
AllData.ignore("**-3.0 5.0-**")
AllData.show()

### values of n: 5, 10, 25
n=35
out = 1
step1 = 0.14
#step2 is calculated so that outer boundry is 400 rg


r = create_r(n,out,step1)
print r
# for surface rings normalization
S = []
for i in range(len(r)):
	Sm = np.pi*(r[i][1]-r[i][0])
	S.append(Sm)

string = create_mo(n)
m = Model(string)

for i in range(n):
	m.setPars({(1+i*18):0.7})
	m(1+i*18).frozen = True
	m(2+i*18).frozen = True
	m(6+i*18).frozen = True
	m(7+i*18).frozen = True
	m(8+i*18).frozen = True
	m(9+i*18).frozen = True
	m(10+i*18).frozen = True
	m(11+i*18).frozen = True
	m(12+i*18).frozen = True
	m(13+i*18).frozen = True
	print i
	rin = 3+i*18
	rout = 5+i*18
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
	val.append(m(18+i*18).values)
	valS.append(m(18+i*18).values[0]/S[i])
	error.append(m(18+i*18).values[1])
	value.append(m(18+i*18).values[0])

x=[]
f = open('values.txt','a')
for i in range(len(val)):
	f.write(str((r[i][0]+r[i][1])/2) + 4*" " + str(val[i]) + "\n") 
	x.append((r[i][0]+r[i][1])/2)
f.close()

"""
f, ax = plt.subplots()		
ax.plot(x,value,".")
ax.set_xlabel("rg")
ax.set_ylabel("N(r)")
ax.set_xscale('log')
ax.set_yscale('log')
ax.errorbar(x ,value, yerr = error, marker = "None", linestyle = "None") #weird stuff
ax.grid(True)
savefig("kyreflionx_spin0.94_log.pdf")
"""

	
plot(x,valS,".")
xlabel("rg")
ylabel("N(r)")
xscale('log')
yscale('log')
errorbar(x ,value, yerr = error, marker = "None", linestyle = "None") #weird stuff
grid(True)
savefig("kyreflionx_surfnorm_spin"+str(spin)+"_step"+str(step1)+".pdf")
show()

