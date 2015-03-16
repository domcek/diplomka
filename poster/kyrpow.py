#!/usr/bin/python
from xspec import *
from pylab import *
import numpy as np


AllModels.initpackage("ky", "lmodel.dat" ,"/mnt/31660B856FD2FABA/xspec/models/KY_code_0/ -udmget64")
AllModels.lmod("ky","/mnt/31660B856FD2FABA/xspec/models/KY_code_0/")
Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/KY_code_0/")
AllModels.setEnergies(".1 50. 1000 log")

def create_r2(n,start,finish):
	r=[]
	step = (finish-start)/n
	b = np.arange(start,finish+step,step)
	for i in range(n):
		k = [np.exp(b[i]),np.exp(b[i+1])]
		r.append(k)
	return r
		
def create_S(r):
	S = []
	for i in range(len(r)):
		Sm = 2*np.pi*(r[i][1]-r[i][0])*(r[i][1]+r[i][0])/2
		S.append(Sm)
	return S

def create_S2(r):
	S = []
	for i in range(len(r)):
		Sm = np.pi*(r[i][1]**2-r[i][0]**2)
		S.append(Sm)
	return S


def create_kyr(n):
	string = "kyrline+"
	new_string = "("
	for i in range(n):
		new_string += string 
		if i == (n-1):
			new_string = new_string[:-1] 
	new_string += "+pow)*phabs"
	return new_string


def fit_kyrpow_S(n,r,S,spin,theta,ms,start,finish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit):
	string = create_kyr(n)

	m = Model(string)
	m.setPars({1+n*12:phoindex,2+n*12:phonorm,3+n*12:nh})
	m(1+n*12).frozen = True
	m(2+n*12).frozen = True
	m(3+n*12).frozen = True
	for i in range(n):
		m.setPars({1+i*12:spin,2+i*12:theta,3+i*12:np.exp(start),4+i*12:ms,5+i*12:np.exp(finish),6+i*12:lineE,7+i*12:0,8+i*12:0,9+i*12:Rbr,10+i*12:z,11+i*12:limb,12+i*12:norm})
		m.setPars({3+i*12:r[i][0],5+i*12:r[i][1]})
		m(1+i*12).frozen = True
		m(2+i*12).frozen = True

	AllModels.show()
	raw_input('Press <ENTER> to continue')
	Fit.nIterations = 10000
	Fit.perform()
	raw_input('Press <ENTER> to continue')

	if err_fit == True:
		stringerr = "maximum 100, "
		for i in range(n):
			stringerr += str(12+i*12)+","
		stringerr = stringerr[:-1]
		Fit.error(stringerr)

	AllModels.show()
	valS = []
	error = []
	x=[]

	for i in range(n):
		valS.append((m(12+i*12).values[0])/S[i])
		x.append((r[i][0]+r[i][1])/2+0.03*(r[i][0]+r[i][1])/2)
		error.append(abs(m(12+i*12).error[0]-m(12+i*12).values[0]))
	
	return x,valS,error



def mainkyr_S(n,spin,theta,ms,start,finish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit):
	m = Model("(kyrline+pow)*phabs")
	m.setPars({1:spin,2:theta,3:np.exp(start),4:ms,5:100,6:lineE,7:alpha,8:beta,9:Rbr,10:z,11:limb,12:norm,13:phoindex,14:phonorm,15:nh})
	AllModels.show()

	fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=3e5)
	AllData.fakeit(1,fs,True,"fakeit_")
	AllModels.setEnergies(".1 10. 1000 log")
	AllData.ignore("**-1.0 10.0-**")
	AllData.show()


	Plot.setRebin("5","10")
	Plot.xAxis = "keV"
	Plot.device = "/xs"
	Plot("ldata")
	

	AllModels.calcFlux("0.1 10")
	Fit.query = "yes"
	AllModels.eqwidth("1")
	raw_input('Press <ENTER> to continue')

	r = create_r2(n,start,finish)
	S = create_S2(r)

	x,y,err = fit_kyrpow_S(n,r,S,spin,theta,ms,start,finish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit)

	print r
	AllModels.calcFlux("0.1 10")
	plot(x,y,".",color="red",label=" ")
	plot(x,y,".",color="red",label="kyrline code 0 with S")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	ylim([10**(-22),10**4])
	if err_fit == True: errorbar(x,y, yerr = err, marker = "+", linestyle = "None") #weird stuff
	grid(True)
	legend()
	
	savefig("./play/kyrline_code_0_normline_100_reduced_10.png")
	show()	
	clf()


n=20
spin = 0.9
theta = 55
start = np.log(2.3)
ms = 1
finish = np.log(10)
lineE = 6.4
alpha = 5
beta = 2
Rbr = 10
z = 4.1e-2
limb = 0 #izotropic
norm = 1e-4 #line
phoindex = 2
phonorm = 1e-2
nh = 1
err_fit = True
#spectrum generated 2.3-100, fitted 2.3 - 10


mainkyr_S(n,spin,theta,ms,start,finish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit)

AllModels.initpackage("ky", "lmodel.dat" ,"/mnt/31660B856FD2FABA/xspec/models/KY_code_-1/ -udmget64")
AllModels.lmod("ky","/mnt/31660B856FD2FABA/xspec/models/KY_code_-1/")
Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/KY_code_-1/")
AllModels.setEnergies(".1 50. 1000 log")

def fit_kyrpow(n,r,S,spin,theta,ms,start,finish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit):
	string = create_kyr(n)
	m = Model(string)
	m.setPars({1+n*12:phoindex,2+n*12:phonorm,3+n*12:nh})
	m(1+n*12).frozen = True
	m(2+n*12).frozen = True
	m(3+n*12).frozen = True
	for i in range(n):
		m.setPars({1+i*12:spin,2+i*12:theta,3+i*12:np.exp(start),4+i*12:ms,5+i*12:np.exp(finish),6+i*12:lineE,7+i*12:0,8+i*12:0,9+i*12:Rbr,10+i*12:z,11+i*12:limb,12+i*12:norm})
		m.setPars({3+i*12:r[i][0],5+i*12:r[i][1]})
		m(1+i*12).frozen = True
		m(2+i*12).frozen = True


	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "maximum 100,"
		for i in range(n):
			stringerr += str(12+i*12)+","
		stringerr = stringerr[:-1]
		Fit.error(stringerr)

	AllModels.show()
	valS = []
	error = []
	x=[]

	for i in range(n):
		valS.append((m(12+i*12).values[0]))
		x.append((r[i][0]+r[i][1])/2+0.03*(r[i][0]+r[i][1])/2)
		error.append(abs(m(12+i*12).error[0]-m(12+i*12).values[0]))
	
	return x,valS,error



def mainkyr(n,spin,theta,ms,start,finish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit):
	m = Model("(kyrline+pow)*phabs")
	#m.setPars({1:lineE,2:Index,3:np.exp(start),4:np.exp(finish),5:theta,6:Rbr,7:index1,8:norm,9:phoindex,10:phonorm,11:1})

	m.setPars({1:spin,2:theta,3:np.exp(start),4:ms,5:100,6:lineE,7:alpha,8:beta,9:Rbr,10:z,11:limb,12:norm,13:phoindex,14:phonorm,15:nh})

	fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=3e5)
	AllData.fakeit(1,fs,True,"fakeit_")
	AllModels.setEnergies(".1 10. 1000 log")
	AllData.ignore("**-1.0 10.0-**")
	AllData.show()
	
	Plot.setRebin("5","10")
	Plot.xAxis = "keV"
	Plot.device = "/xs"
	Plot("ldata")
	
	AllModels.calcFlux("0.1 10")
	Fit.query = "yes"
	AllModels.eqwidth("1")
	raw_input('Press <ENTER> to continue')

	r = create_r2(n,start,finish)
	S = create_S2(r)

	x,y,err = fit_kyrpow(n,r,S,spin,theta,ms,start,finish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit)

	print r
	AllModels.calcFlux("0.1 10")
	plot(x,y,".",color="blue",label="kyrline code -1 without S")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	ylim([10**(-22),10**4])
	if err_fit == True: errorbar(x,y, yerr = err, marker = "+", linestyle = "None") #weird stuff
	grid(True)
	legend()
	
	savefig("./play/kyrline_code_-1_normline_100_reduced_10.png")
	show()	
	clf()


mainkyr(n,spin,theta,ms,start,finish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit)
