#!/usr/bin/python
from xspec import *
from pylab import *
import numpy as np
from scipy.optimize import curve_fit
 
def powerlaw(x,a,b):
	return a*x+b

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
	Fit.nIterations = 10000
	Fit.perform()
#	raw_input('Press <ENTER> to continue')

	if err_fit == True:
		stringerr = "maximum 100000, "
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
		x.append((r[i][0]+r[i][1])/2)
		error.append(abs(m(12+i*12).error[0]-m(12+i*12).values[0]))
		print abs(m(12+i*12).error[0])
	
	return x,valS,error

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
#	raw_input('Press <ENTER> to continue')

	if err_fit == True:
		stringerr = "maximum 100000,"
		for i in range(n):
			stringerr += str(12+i*12)+","
		stringerr = stringerr[:-1]
		Fit.error(stringerr)

	AllModels.show()
	val = []
	error = []
	x=[]

	for i in range(n):
		val.append((m(12+i*12).values[0]))
		x.append((r[i][0]+r[i][1])/2)#+0.03*(r[i][0]+r[i][1])/2)
		error.append(abs(m(12+i*12).error[0]-m(12+i*12).values[0])) #xspec returns errors in format with down and up limit, it is necessary to substract average fitted value to get errors into python
		print m(12+i*12).error
		print m(12+i*12).error[0], m(12+i*12).values[0]
		print m(12+i*12).error[1]

	raw_input('Press <ENTER> to continue')

	
	return x,val,error

def not_broken(n,k,spin,theta,ms,start,fitfinish,modelfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit,broken,model):
	#if time delete _in
	r_in = create_r2(n,start,fitfinish)
	S_in = create_S2(r_in)

	if model == -1:	
		x_in,y_in,err_in = fit_kyrpow(n,r_in,S_in,spin,theta,ms,start,fitfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit)

	if model == 0:
		x_in,y_in,err_in = fit_kyrpow_S(n,r_in,S_in,spin,theta,ms,start,fitfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit)

	xl_in = np.log10(x_in)
	yl_in = np.log10(y_in)
	derivation_const = 0.434
	errl_in = []
	if err_fit == True:
		for i in range(len(err_in)):
			errl_in.append(abs(derivation_const*err_in[i]/y_in[i])) #relative error of loglog scale


	popt_in, pcov_in = curve_fit(powerlaw, xl_in, yl_in)
	print popt_in
	return x_in,y_in,err_in,xl_in,yl_in,errl_in,popt_in,pcov_in

def is_broken(n,k,spin,theta,ms,start,fitfinish,modelfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit,broken,model):
	r_in = create_r2(n,start,fitfinish)
	S_in = create_S2(r_in)

	if model == -1:	
		x_in,y_in,err_in = fit_kyrpow(n,r_in,S_in,spin,theta,ms,start,fitfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit)

	if model == 0:
		x_in,y_in,err_in = fit_kyrpow_S(n,r_in,S_in,spin,theta,ms,start,fitfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit)	

	xl_in = np.log10(x_in)
	yl_in = np.log10(y_in)
	derivation_const = 0.434
	errl_in = []
	if err_fit == True:
		for i in range(len(err_in)):
			errl_in.append(abs(derivation_const*err_in[i]/y_in[i])) #relative error of loglog scale


	popt_in, pcov_in = curve_fit(powerlaw, xl_in, yl_in)

	r_out = create_r2(k,fitfinish,modelfinish)
	S_out = create_S2(r_out)
	print r_out
	if model == -1:	
		x_out,y_out,err_out = fit_kyrpow(k,r_out,S_out,spin,theta,ms,fitfinish,modelfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit)

	if model == 0:	
		x_out,y_out,err_out = fit_kyrpow_S(k,r_out,S_out,spin,theta,ms,fitfinish,modelfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit)
		
	xl_out = np.log10(x_out)
	yl_out = np.log10(y_out)
	errl_out = []
	if err_fit == True:
		for i in range(len(err_out)):
			errl_out.append(abs(derivation_const*err_out[i]/y_out[i])) #relative error of loglog scale

	popt_out, pcov_out = curve_fit(powerlaw, xl_out, yl_out)
	print popt_out

	xl,yl,errl,err = [[] for i in range(4)]
	#joining lists
	x = x_in + x_out
	y = y_in + y_out
	if err_fit == True: err = err_in + err_out
	for i in range(len(xl_in)):
		xl.append(xl_in[i])
		yl.append(yl_in[i])
		if err_fit == True: errl.append(errl_in[i])
	for i in range(len(xl_out)):
		xl.append(xl_out[i])
		yl.append(yl_out[i])
		if err_fit == True: errl.append(errl_out[i])

	return x,y,err,xl,yl,errl,x_in,y_in,err_in,xl_in,yl_in,errl_in,popt_in,pcov_in,x_out,y_out,err_out,xl_out,yl_out,errl_out,popt_out,pcov_out


#pozor na log errory v xspecu

def mainkyr(n,k,spin,theta,ms,start,fitfinish,modelfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit,broken):
#	AllModels.initpackage("ky", "lmodel.dat" ,"/mnt/31660B856FD2FABA/xspec/models/KY_code_-1/ -udmget64")
	AllModels.lmod("ky","/mnt/31660B856FD2FABA/xspec/models/KY_code_-1/")
	Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/KY_code_-1/")
	AllModels.setEnergies(".1 50. 1000 log")

	m = Model("(kyrline+pow)*phabs")
	#m.setPars({1:lineE,2:Index,3:np.exp(start),4:np.exp(finish),5:theta,6:Rbr,7:index1,8:norm,9:phoindex,10:phonorm,11:1})

	m.setPars({1:spin,2:theta,3:np.exp(start),4:ms,5:np.exp(modelfinish),6:lineE,7:alpha,8:beta,9:Rbr,10:z,11:limb,12:norm,13:phoindex,14:phonorm,15:nh})

	fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=3e5)
	AllData.fakeit(1,fs,True,"fakeit_")
	AllModels.setEnergies(".1 10. 1000 log")
	AllData.ignore("**-1.0 10.0-**")
	AllData.show()
	
	"""
	Plot.setRebin("5","10")
	Plot.xAxis = "keV"
	Plot.device = "/xs"
	Plot("ldata")
	"""

	AllModels.calcFlux("0.1 10")
	Fit.query = "yes"
	AllModels.eqwidth("1")
	raw_input('Press <ENTER> to continue')

	model = -1
	##until break fit radius
	if broken == False: 
		x,y,err,xl,yl,errl,popt,pcov = not_broken(n,k,spin,theta,ms,start,fitfinish,modelfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit,broken,model)

	if broken == True:
		x,y,err,xl,yl,errl,x_in,y_in,err_in,xl_in,yl_in,errl_in,popt_in,pcov_in,x_out,y_out,err_out,xl_out,yl_out,errl_out,popt_out,pcov_out = is_broken(n,k,spin,theta,ms,start,fitfinish,modelfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit,broken,model)
		

#	AllModels.initpackage("ky", "lmodel.dat" ,"/mnt/31660B856FD2FABA/xspec/models/KY_code_0/ -udmget64")
	"""
	AllModels.lmod("ky","/mnt/31660B856FD2FABA/xspec/models/KY_code_0/")
	Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/KY_code_0/")
	AllModels.setEnergies(".1 50. 1000 log")

	model = 0
	if broken == False: 
		x0,y0,err0,x0l,y0l,err0l,popt0,pcov0 = not_broken(n,k,spin,theta,ms,start,fitfinish,modelfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit,broken,model)

	if broken == True:
		x0,y0,err0,x0l,y0l,err0l,x0_in,y0_in,err0_in,x0l_in,y0l_in,err0l_in,popt0_in,pcov0_in,x0_out,y0_out,err0_out,x0l_out,y0l_out,err0l_out,popt0_out,pcov0_out = is_broken(n,k,spin,theta,ms,start,fitfinish,modelfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit,broken,model)
	"""	

	AllModels.calcFlux("0.1 10")
	if broken == True:
		plot(xl,yl,".",color="blue",label="kyrline code -1 without S, index. "+str(popt_in[0])+" index2. "+str(popt_out[0]))
		plot(xl_in,powerlaw(xl_in,*popt_in),'b--')
		plot(xl_out,powerlaw(xl_out,*popt_out),'b--')

	if broken == False:
		plot(xl,yl,".",color="blue",label="kyrline code -1 without S, index = "+str(popt[0])+"+/-"+str(pcov[0][0]))
		plot(xl,powerlaw(xl,*popt),'b--')

	"""
	if broken == True:
		plot(x0l,y0l,".",color="red",label="kyrline code 0 with S index. "+str(popt0_in[0])+" index2. "+str(popt0_out[0]))
		plot(x0l_in,powerlaw(x0l_in,*popt0_in),'r--')
		plot(x0l_out,powerlaw(x0l_out,*popt0_out),'r--')
		#kod na down limit errorbar(x+0.6, y, xerr=0.1, xuplims=upperlimits, xlolims=lowerlimits)

	if broken == False:
		plot(x0l,y0l,".",color="red",label="kyrline code 0 with S, index = "+str(popt0[0])+"+/-"+str(pcov0[0][0]))
		plot(x0l,powerlaw(x0l,*popt0),'r--')
	"""

	xlabel("rg")
	ylabel("N(r)")

	#ylim([10**(-22),10**4])
	if err_fit == True: errorbar(xl,yl, yerr = errl, marker = "+", linestyle = "None") #weird stuff
	#if err_fit == True: errorbar(x0l,y0l, yerr = err0l, marker = "+", linestyle = "None") #weird stuff
	grid(True)
	legend()
	savefig("./play/kyrline_normline_"+str(norm)+"_phonorm_"+str(phonorm)+"fit.png")
	show()	
	clf()

	plot(x,y,".",color="blue",label="kyrline code -1 without S")
	#plot(x0,y0,".",color="red",label="kyrline code 0 with S")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log',nonposy='clip')

	#ylim([10**(-22),10**4])
	if err_fit == True: errorbar(x,y, yerr = errl, marker = "+", linestyle = "None") #weird stuff
	#if err_fit == True: errorbar(x0,y0, yerr = err0l, marker = "+", linestyle = "None") #weird stuff
	grid(True)
	legend()
	#savefig("./play/kyrline_normline_"+str(norm)+"_phonorm_"+str(phonorm)+".png")
	show()	
	clf()


n=5
k = 5 # out parameter
spin = 0.9
theta = 55
start = np.log(2.3)
modelfinish = np.log(10)
ms = 1
fitfinish = np.log(5)
lineE = 6.4
alpha = 5
beta = 2
Rbr = 10
z = 4.1e-2
limb = 0 #izotropic
norm = 1e-1 #line
phoindex = 2
phonorm = 1e-3
nh = 1
err_fit = True
broken = True #if false, need to have modelfinish and fitfinish same
#spectrum generated 2.3-100, fitted 2.3 - 10

mainkyr(n,k,spin,theta,ms,start,fitfinish,modelfinish,lineE,alpha,beta,Rbr,z,limb,norm,phoindex,phonorm,nh,err_fit,broken)
