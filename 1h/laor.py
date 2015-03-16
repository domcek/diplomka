#!/usr/bin/python
from xspec import *
from pylab import *
import numpy as np

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

def create_laor(n):
	string = "laor+"
	new_string = ""
	for i in range(n):
		new_string += string 
		if i == (n-1):
			new_string = new_string[:-1] 
	return new_string

def create_laorpow(n):
	string = "laor+"
	new_string = "("
	for i in range(n):
		new_string += string 
		if i == (n-1):
			new_string = new_string[:-1] 
	new_string += "+pow)*phabs"
	return new_string

def create_laor2(n):
	string = "laor2+"
	new_string = ""
	for i in range(n):
		new_string += string 
		if i == (n-1):
			new_string = new_string[:-1] 
	return new_string

def create_laor2pow(n):
	string = "laor2+"
	new_string = "("
	for i in range(n):
		new_string += string 
		if i == (n-1):
			new_string = new_string[:-1] 
	new_string += "+pow)*phabs"
	return new_string

def little_help(n,r,p11,q):
	hlp = []
	for i in range(n):
		rr = (r[i][0]+r[i][1])/2
		hlp.append(p11*rr**(-q))
	return hlp

def fit_laor(n,lineE,Index,start,finish,theta,norm,r,S,err_fit):
	string = create_laor(1)
	m = Model(string)
	m.setPars({3:r[0][0],4:r[0][1]})
	m.setPars({1:lineE,2:Index,3:np.exp(start),4:np.exp(finish),5:theta,6:norm})
	m(1).frozen = False
	m(2).frozen = False
	m(3).frozen = True
	m(4).frozen = True
	m(5).frozen = False
	m(6).frozen = False

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	p1 = m(1).values[0]
	p2 = m(2).values[0]
	p5 = m(5).values[0]
	p6 = m(6).values[0]

	AllModels.show()

	raw_input('Press <ENTER> to continue')
	hlp = little_help(n,r,p6,p2)

	string = create_laor(n)
	m = Model(string)
	for i in range(n):
		m.setPars({3+i*6:r[i][0],4+i*6:r[i][1]})
		m.setPars({1+i*6:p1,2+i*6:0,5+i*6:p5,6+i*6:hlp[i]})
		m(1+i*6).frozen = True
		m(2+i*6).frozen = True
		m(3+i*6).frozen = True
		m(4+i*6).frozen = True
		m(5+i*6).frozen = True
		m(6+i*6).frozen = False

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "maximum 100,"
		for i in range(n):
			stringerr += str(6+i*6)+","
		stringerr = stringerr[:-1]
		Fit.error(stringerr)

	valS = []
	error = []
	x=[]


	for i in range(n):
		valS.append((m(6+i*6).values[0])/(S[i]))
		x.append((r[i][0]+r[i][1])/2+0.03*(r[i][0]+r[i][1])/2)
		error.append(abs(m(6+i*6).error[0]-m(6+i*6).values[0]))
	
	return x,valS,error

def main(n,lineE,Index,start,finish,theta,norm,err_fit):
	m = Model("laor")
	m.setPars({1:lineE,2:Index,3:np.exp(start),4:np.exp(finish),5:theta,6:norm})

	fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=3e5)
	AllData.fakeit(1,fs,True,"fakeit_")
	AllModels.setEnergies(".1 10. 1000 log")
	AllData.ignore("**-1.0 10.0-**")
	AllData.show()
	
	AllModels.calcFlux("0.1 10")
	Fit.query = "yes"
	raw_input('Press <ENTER> to continue')

	
	r = create_r2(n,start,finish)
	S = create_S(r)

	x,y,err = fit_laor(n,lineE,Index,start,finish,theta,norm,r,S,err_fit)

	print r
	AllModels.calcFlux("0.1 10")
	plot(x,y,".",color="red",label="laor")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	ylim([10**(-22),10**4])
	if err_fit == True: errorbar(x,y, yerr = err, marker = "+", linestyle = "None") #weird stuff
	grid(True)
	legend()
	show()
	savefig("./play/laor.png")	
	clf()

def fit_laor2(n,r,S,lineE,Index,start,finish,theta,Rbr,index1,norm,err_fit):
	string = create_laor2(1)
	m = Model(string)
	m.setPars({1:lineE,2:Index,3:np.exp(start),4:np.exp(finish),5:theta,6:Rbr,7:index1,8:norm})
	m(1).frozen = False
	m(2).frozen = False
	m(3).frozen = True
	m(4).frozen = True
	m(5).frozen = False
	m(6).frozen = False
	m(7).frozen = False
	m(8).frozen = False

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	p1 = m(1).values[0]
	p2 = m(2).values[0]
	p5 = m(5).values[0]
	p6 = m(6).values[0]
	p7 = m(7).values[0]
	p8 = m(8).values[0]
	print p7
	hlp = little_help(n,r,p8,p2)

	string = create_laor2(n)
	m = Model(string)
	for i in range(n):
		m.setPars({3+i*8:r[i][0],4+i*8:r[i][1]})
		m.setPars({1+i*8:p1,2+i*8:0,5+i*8:p5,6+i*8:p6,7+i*8:p7,8+i*8:hlp[i]})
		m(1+i*8).frozen = True
		m(2+i*8).frozen = True
		m(3+i*8).frozen = True
		m(4+i*8).frozen = True
		m(5+i*8).frozen = True
		m(6+i*8).frozen = True
		m(7+i*8).frozen = True
		m(8+i*8).frozen = False

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "maximum 100,"
		for i in range(n):
			stringerr += str(8+i*8)+","
		stringerr = stringerr[:-1]
		Fit.error(stringerr)

	valS = []
	error = []
	x=[]


	for i in range(n):
		valS.append((m(8+i*8).values[0])/(S[i]))
		x.append((r[i][0]+r[i][1])/2+0.03*(r[i][0]+r[i][1])/2)
		error.append(abs(m(8+i*8).error[0]-m(8+i*8).values[0]))
	
	return x,valS,error


def mainlaor2(n,lineE,Index,start,finish,theta,Rbr,index1,norm,err_fit):
	m = Model("laor2")
	m.setPars({1:lineE,2:Index,3:np.exp(start),4:np.exp(finish),5:theta,6:Rbr,7:index1,8:norm})

	fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=3e5)
	AllData.fakeit(1,fs,True,"fakeit_")
	AllModels.setEnergies(".1 10. 1000 log")
	AllData.ignore("**-1.0 10.0-**")
	AllData.show()
	
	AllModels.calcFlux("0.1 10")
	Fit.query = "yes"

	Plot.setRebin("5","10")
	Plot.xAxis = "keV"
	Plot.device = "/xs"
	Plot("data")
	
	r = create_r2(n,start,finish)
	S = create_S(r)

	x,y,err = fit_laor2(n,r,S,lineE,Index,start,finish,theta,Rbr,index1,norm,err_fit)

	print r
	AllModels.calcFlux("0.1 10")
	plot(x,y,".",color="red",label="laor")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	ylim([10**(-22),10**4])
	if err_fit == True: errorbar(x,y, yerr = err, marker = "+", linestyle = "None") #weird stuff
	grid(True)
	legend()
	show()
	savefig("./play/laor.png")	
	clf()

def fit_laorpow(n,lineE,Index,start,finish,theta,norm,r,S,err_fit,phoindex,phonorm):
	string = create_laorpow(1)
	m = Model(string)

	m.setPars({1:lineE,2:Index,3:np.exp(start),4:np.exp(finish),5:theta,6:norm,7:phoindex,8:phonorm,9:1})
	m(1).frozen = False
	m(2).frozen = False
	m(3).frozen = True
	m(4).frozen = True
	m(5).frozen = False
	m(6).frozen = False
	m(7).frozen = False
	m(8).frozen = False
	m(9).frozen = False

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	p1 = m(1).values[0]
	p2 = m(2).values[0]
	p5 = m(5).values[0]
	p6 = m(6).values[0]
	p7 = m(7).values[0]
	p8 = m(8).values[0]
	p9 = m(9).values[0]

	hlp = little_help(n,r,p6,p2)
	AllModels.show()
	raw_input('Press <ENTER> to continue')
	string = create_laorpow(n)
	m = Model(string)

	m.setPars({1+n*6:p7,2+n*6:p8,3+n*6:p9})
	m(1+n*6).frozen = True
	m(2+n*6).frozen = True
	m(3+n*6).frozen = True
	for i in range(n):
		m.setPars({3+i*6:r[i][0],4+i*6:r[i][1]})
		m.setPars({1+i*6:p1,2+i*6:0,5+i*6:p5,6+i*6:hlp[i]})
		m(1+i*6).frozen = True
		m(2+i*6).frozen = True
		m(3+i*6).frozen = True
		m(4+i*6).frozen = True
		m(5+i*6).frozen = True
		m(6+i*6).frozen = False

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "maximum 100,"
		for i in range(n):
			stringerr += str(6+i*6)+","
		stringerr = stringerr[:-1]
		Fit.error(stringerr)

	valS = []
	error = []
	x=[]


	for i in range(n):
		valS.append((m(6+i*6).values[0])/(S[i]))
		x.append((r[i][0]+r[i][1])/2+0.03*(r[i][0]+r[i][1])/2)
		error.append(abs(m(6+i*6).error[0]-m(6+i*6).values[0]))
	
	return x,valS,error

def mainpow(n,lineE,Index,start,finish,theta,norm,err_fit,phoindex,phonorm):
	m = Model("(laor+pow)*phabs")
	m.setPars({1:lineE,2:Index,3:np.exp(start),4:np.exp(finish),5:theta,6:norm,7:phoindex,8:phonorm,9:1})

	fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=3e5)
	AllData.fakeit(1,fs,True,"fakeit_")
	AllModels.setEnergies(".1 10. 1000 log")
	AllData.ignore("**-1.0 10.0-**")
	AllData.show()
	
	AllModels.calcFlux("0.1 10")
	Fit.query = "yes"
	AllModels.eqwidth("1")
	raw_input('Press <ENTER> to continue')

	
	r = create_r2(n,start,finish)
	S = create_S(r)

	x,y,err = fit_laorpow(n,lineE,Index,start,finish,theta,norm,r,S,err_fit,phoindex,phonorm)
	AllModels.calcFlux("0.1 10")
	plot(x,y,".",color="red",label="laor")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	ylim([10**(-22),10**4])
	if err_fit == True: errorbar(x,y, yerr = err, marker = "+", linestyle = "None") #weird stuff
	grid(True)
	legend()
	show()
	savefig("./play/laor.png")	
	clf()



def fit_laor2pow(n,r,S,lineE,Index,start,finish,theta,Rbr,index1,norm,err_fit):
	string = create_laor2pow(1)
	m = Model(string)
	m.setPars({1:lineE,2:Index,3:np.exp(start),4:np.exp(finish),5:theta,6:Rbr,7:index1,8:norm,9:phoindex,10:phonorm,11:1})
	m(1).frozen = False
	m(2).frozen = False
	m(3).frozen = True
	m(4).frozen = True
	m(5).frozen = False
	m(6).frozen = True
	m(7).frozen = False
	m(8).frozen = False
	m(9).frozen = False
	m(10).frozen = False
	m(11).frozen = False

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	p1 = m(1).values[0]
	p2 = m(2).values[0]
	p5 = m(5).values[0]
	p6 = m(6).values[0]
	p7 = m(7).values[0]
	p8 = m(8).values[0]
	p9 = m(9).values[0]
	p10 = m(10).values[0]
	p11 = m(11).values[0]
	print p7
	hlp = little_help(n,r,p8,p2)
	AllModels.show()
	raw_input('Press <ENTER> to continue')

	string = create_laor2pow(n)
	m = Model(string)
	m.setPars({1+n*8:p9,2+n*8:p10,3+n*8:p11})
	m(1+n*8).frozen = True
	m(2+n*8).frozen = True
	m(3+n*8).frozen = True
	for i in range(n):
		m.setPars({3+i*8:r[i][0],4+i*8:r[i][1]})
		m.setPars({1+i*8:p1,2+i*8:0,5+i*8:p5,6+i*8:p6,7+i*8:p7,8+i*8:hlp[i]})
		m(1+i*8).frozen = True
		m(2+i*8).frozen = True
		m(3+i*8).frozen = True
		m(4+i*8).frozen = True
		m(5+i*8).frozen = True
		m(6+i*8).frozen = True
		m(7+i*8).frozen = True
		m(8+i*8).frozen = False

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "maximum 100,"
		for i in range(n):
			stringerr += str(8+i*8)+","
		stringerr = stringerr[:-1]
		Fit.error(stringerr)

	valS = []
	error = []
	x=[]


	for i in range(n):
		valS.append((m(8+i*8).values[0])/(S[i]))
		x.append((r[i][0]+r[i][1])/2+0.03*(r[i][0]+r[i][1])/2)
		error.append(abs(m(8+i*8).error[0]-m(8+i*8).values[0]))
	
	return x,valS,error


def mainlaor2pow(n,lineE,Index,start,finish,theta,Rbr,index1,norm,err_fit,phoindex,phonorm):
	m = Model("(laor2+pow)*phabs")
	m.setPars({1:lineE,2:Index,3:np.exp(start),4:np.exp(finish),5:theta,6:Rbr,7:index1,8:norm,9:phoindex,10:phonorm,11:1})

	fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=3e5)
	AllData.fakeit(1,fs,True,"fakeit_")
	AllModels.setEnergies(".1 10. 1000 log")
	AllData.ignore("**-1.0 10.0-**")
	AllData.show()
	
	Plot.setRebin("5","10")
	Plot.xAxis = "keV"
	Plot.device = "/xs"
	Plot("lmodel")
	
	AllModels.calcFlux("0.1 10")
	Fit.query = "yes"
	AllModels.eqwidth("1")
	raw_input('Press <ENTER> to continue')


	r = create_r2(n,start,finish)
	S = create_S(r)

	x,y,err = fit_laor2pow(n,r,S,lineE,Index,start,finish,theta,Rbr,index1,norm,err_fit)
	AllModels.calcFlux("0.1 10")
	plot(x,y,".",color="red",label="laor")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	ylim([10**(-22),10**4])
	if err_fit == True: errorbar(x,y, yerr = err, marker = "+", linestyle = "None") #weird stuff
	grid(True)
	legend()
	show()
	savefig("./play/laor.png")	
	clf()

	
n = 25
#laor 1
lineE = 6.4
Index = 6
start = log(1.235)
finish = log(400)
theta = 55
norm = 6e-4
err_fit = False

#+pow
phoindex = 2
phonorm = 1e-2


#main(n,lineE,Index,start,finish,theta,norm,err_fit)

#mainpow(n,lineE,Index,start,finish,theta,norm,err_fit,phoindex,phonorm)

#laor2
Index = 4
index1 = 2
Rbr = 5
norm = 1e-2
phonorm = 3e-2

#mainlaor2(n,lineE,Index,start,finish,theta,Rbr,index1,norm,err_fit)

mainlaor2pow(n,lineE,Index,start,finish,theta,Rbr,index1,norm,err_fit,phoindex,phonorm)