#!/usr/bin/python
from xspec import *
from pylab import *
import numpy as np

def create_mo(n):
	string = "kdblur*atable{/mnt/31660B856FD2FABA/xspec/models/reflionx/reflionx.mod}+"
	new_string = ""
	for i in range(n):
		new_string += string 
		if i == (n-1):
			new_string = new_string[:-1] 
	return new_string

def create_r(n,out,step1):
	r=[]
	
	start = 1.5
	end = start+(n-out)*step1
	b = np.arange(start,end,step1)
	step2 = (5.8-b[-1]-step1)/out
	c = np.arange(b[-1]+step1, 6+step2, step2)
	b = np.append(b, c)

	for i in range(n):
		k = [np.exp(b[i]),np.exp(b[i+1])]
		r.append(k)
	return r

n=1
string = create_mo(n)
m = Model(string)
m.setPars({2:4.4,3:400})

#AllModels.initpackage("kyreflionx", "lmodel.dat" ,"/mnt/31660B856FD2FABA/xspec/models/kyreflionx/ -udmget64")
AllModels.setEnergies(".1 50. 1000 log")

fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=1e5)
AllData.fakeit(1,fs,False,"fakeit_") #True/False is about applied statistics
AllModels.setEnergies(".1 10. 1000 log")
AllData.ignore("**-3.0 5.0-**")
AllData.show()


### Part 2, fit the average emisivity

n=1
string = create_mo(n)
m = Model(string)

m(4).frozen = True
m(5).frozen = True
m(6).frozen = True
m(9).frozen = True

Fit.nIterations = 100000
Fit.perform()
xi = m(7).values[0]
print xi

### Part 3, fit by sum of kdblur and reflionx

n=25
out = 1
step1 = 0.05

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
	m(4+i*9).frozen = True
	m(5+i*9).frozen = True
	m(6+i*9).frozen = True
	m.setPars({(7+i*9):xi})
	m(7+i*9).frozen = True

	print i
	rin = 2+i*9
	rout = 3+i*9
	print rin, r[i][0]
	print rout, r[i][1]
	m.setPars({rin:r[i][0],rout:r[i][1]})

AllModels.show()

Fit.nIterations = 100000
Fit.perform()
"""
for i in range(n):
	string = "max 1000 "+str(18+i*18)
	Fit.error(string)
"""

val = []
valS = []
value = []
error = []
for i in range(n):
	val.append(m(9+i*9).values)
	valS.append(m(9+i*9).values[0]/S[i])
	error.append(m(9+i*9).values[1])
	value.append(m(9+i*9).values[0])

x=[]
#f = open('values.txt','a')
for i in range(len(val)):
	#f.write(str((r[i][0]+r[i][1])/2) + 4*" " + str(val[i]) + "\n") 
	x.append((r[i][0]+r[i][1])/2)
#f.close()


f, ax = plt.subplots()		
ax.plot(x,value,".")
ax.set_xlabel("rg")
ax.set_ylabel("N(r)")
ax.set_xscale('log')
ax.set_yscale('log')
ax.errorbar(x ,value, yerr = error, marker = "None", linestyle = "None") #weird stuff
ax.grid(True)
savefig("kdref_log.pdf")

f, ax = plt.subplots()		
ax.plot(x,valS,".")
ax.set_xlabel("rg")
ax.set_ylabel("N(r)")
ax.set_xscale('log')
ax.set_yscale('log')
ax.errorbar(x ,value, yerr = error, marker = "None", linestyle = "None") #weird stuff
ax.grid(True)
savefig("kdref_surfnorm_log.pdf")
show()

