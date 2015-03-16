#!/usr/bin/python
from xspec import *
from pylab import *
import numpy as np


def create_r(n,out,start,finish,step1):
	r=[]
	end = start+(n-out)*step1
	b = np.arange(start,end,step1)
	step2 = (finish-b[-1]-step1)/out #step2 is calculated so that outer boundry is 100 rg (that is why constant 4.6 is used)
	c = np.arange(b[-1]+step1, finish+step2, step2)
	b = np.append(b, c)
	# surface rings normalization
	for i in range(n):
		k = [np.exp(b[i]),np.exp(b[i+1])]
		r.append(k)
	return r

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

def create_mokyx(n):
	string = "kyreflionx+"
	new_string = ""
	for i in range(n):
		new_string += string 
		if i == (n-1):
			new_string = new_string[:-1] 
	return new_string

def create_mokdref(n,machine):
	if machine == "home": string = "kdblur*atable{/mnt/31660B856FD2FABA/xspec/models/reflionx/reflionx.mod}+"
	if machine == "elp": string = "kdblur*atable{/home/domcek/xspec/models/reflionx/reflionx.mod}+"
	new_string = "("
	for i in range(n):
		new_string += string 
		if i == (n-1):
			new_string = new_string[:-1] 
	new_string += "+pow)*phabs"
	return new_string

#############################################publication testing###################################################
def pubfit_kdrelavgvar_v2(n,r,S,spin,theta,height,phoindex,iron,ionisation,absorption,z,norm,err_fit):
	s = 1
	string = create_mokdref(s,machine)
	m = Model(string)

	m(1).frozen = True
	m.setPars({1:0,2:np.exp(start),3:np.exp(finish),4:theta,5:iron,7:ionisation,8:z,9:norm})
	m(4).frozen = False
	m(5).frozen = False
	m(6).frozen = False
	m(9).frozen = False
	m(8).frozen = False
	m.setPars({1+s*9:phoindex,2+s*9:norm,3+s*9:absorption})
	m(6).link = "10"

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	p4 = m(4).values[0]
	p5 = m(5).values[0]
	p6 = m(6).values[0]
	p7 = m(7).values[0]
	p8 = m(8).values[0]
	p9 = m(9).values[0]
	p10 = m(10).values[0]
	p11 = m(11).values[0]
	p12 = m(12).values[0]


	
	string = create_mokdref(n,machine)
	m = Model(string)

	m.setPars({1+n*9:p10,2+n*9:p11,3+n*9:p12})
	m(1+n*9).frozen = True
	m(2+n*9).frozen = True
	m(3+n*9).frozen = True
	
	for i in range(n):
		m.setPars({1+i*9:0,4+i*9:p4,5+i*9:p5,6+i*9:p6,7+i*9:p7,8+i*9:p8,9+i*9:p9})
		m(4+i*9).frozen = True
		m(5+i*9).frozen = True
		m(6+i*9).link = str(1+n*9)
		m(6+i*9).frozen = True
		m(7+i*9).frozen = True

		rin = 2+i*9
		rout = 3+i*9
		print i
		print rin, r[i][0]
		print rout, r[i][1]
		m.setPars({rin:r[i][0],rout:r[i][1]})



	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = ""
		for i in range(n):
			stringerr += str(9+i*9)+","
		stringerr = stringerr[:-1]
		Fit.error(stringerr)

	valS = []
	error = []
	x=[]

	for i in range(n):
		valS.append((m(9+i*9).values[0])/(S[i]))
		x.append((r[i][0]+r[i][1])/2)
		error.append((m(9+i*9).error[0]+m(9+i*9).error[1])/2)
	
	return x,valS,error

def pubfit_kdrelavgvar_v1(n,r,S,spin,theta,height,phoindex,iron,ionisation,absorption,z,norm,err_fit):
	string = create_mokdref(n,machine)
	m = Model(string)
	"""
	m(1).frozen = True
	m.setPars({1:2,2:np.exp(start),3:np.exp(finish),4:theta,5:iron,7:ionisation,8:z,9:norm})
	m(4).frozen = True
	m(5).frozen = True
	m(6).frozen = True
	m(9).frozen = False
	m.setPars({1+s*9:phoindex,2+s*9:norm,3+s*9:absorption})
	m(6).link = "10"
	"""

	m.setPars({1+n*9:phoindex,2+n*9:norm,3+n*9:absorption})
	m(1+n*9).frozen = True
	m(2+n*9).frozen = True
	m(3+n*9).frozen = True

	for i in range(n):
		m.setPars({1+i*9:0,4+i*9:theta,5+i*9:iron,6+i*9:phoindex,7+i*9:ionisation,8+i*9:z,9+i*9:norm})
		m(4+i*9).frozen = True
		m(5+i*9).frozen = True
		m(6+i*9).link = str(1+n*9)
		m(6+i*9).frozen = True
		m(7+i*9).frozen = True

		rin = 2+i*9
		rout = 3+i*9
		print i
		print rin, r[i][0]
		print rout, r[i][1]
		m.setPars({rin:r[i][0],rout:r[i][1]})

	


	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "stopat 10000,"
		for i in range(n):
			stringerr += str(9+i*9)+","
		stringerr = stringerr[:-1]
		Fit.error(stringerr)

	valS = []
	error = []
	x=[]

	for i in range(n):
		valS.append((m(9+i*9).values[0])/(S[i]))
		x.append((r[i][0]+r[i][1])/2)
		error.append((m(9+i*9).error[0]+m(9+i*9).error[1])/2)

	return x,valS,error

def pub(spin,theta,height,phoindex,index,iron,ionisation,z,absorption,norm,n,out,step1,start,finish,err_fit):
	###Creating model (kdblur+reflionx+pow)*phabs
	s=1
	string = create_mokdref(s,machine)
	m = Model(string)
	m(1).frozen = True
	m.setPars({1:index,2:np.exp(start),3:np.exp(finish),4:theta,5:iron,7:ionisation,8:z,9:norm})
	m(4).frozen = True
	m(5).frozen = True
	m(6).frozen = True
	m(9).frozen = False
	m.setPars({1+s*9:phoindex,2+s*9:norm,3+s*9:absorption})
	m(6).link = "10"

	fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=3e5)
	AllData.fakeit(1,fs,True,"fakeit_")
	AllModels.setEnergies(".1 10. 1000 log")
	AllData.ignore("**-1.0 10.0-**")
	AllData.show()

	AllModels.show()
	AllModels.calcFlux("0.1 10")

	###Fit model

	r = create_r(n,out,start,finish,step1)
	S = create_S(r)

	
	rx,ry,err_r = 0,0,0
	rx,ry,err_r = pubfit_kdrelavgvar_v1(n,r,S,spin,theta,height,phoindex,iron,ionisation,absorption,z,norm,err_fit)

	plot(rx,ry,".",color="red",label="kdblur+reflionx,xi=const")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	ylim([10**(-22),10**4])
	if err_fit == True: errorbar(rx ,ry, yerr = err_r, marker = "None", linestyle = "None") #weird stuff
	#errorbar(rxvar,ryvar, yerr = err_rvar, marker = "None", linestyle = "None") #weird stuff
	grid(True)
	legend()
	savefig("./play/compare_sp_"+str(spin)+"th_"+str(theta)+"h_"+str(height)+"phoi_"+str(phoindex)+"n_"+str(n)+"out_"+str(out)+"step1_"+str(step1)+"start_"+str(start)+".png")
	show()
	clf()


def fit_kdxill(n,index,iron,ionisation,z,absorption,norm,r,S,spin,theta,height,phoindex,err_fit):
	s=1
	string = create_mokdxill(s,machine)
	m = Model(string)


	m(1).frozen = False #don't care but better free
	m.setPars({1:0,4:theta,5:phoindex,6:iron,10:z})


	##free parameters index (1), ionization (8), norm(11)
	m.setPars({1:0,2:r[0][0],3:r[n-1][1]})
	m(9).link = "4"
	m(4).frozen = True
	m(5).frozen = True
	m(6).frozen = True
	m(7).frozen = False
	m(8).frozen = True
	m(11).frozen = False
	m.setPars({1+s*11:phoindex,2+s*11:1,3+s*11:1})
	m(12).frozen = False
	m(5).link = "12"

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	q = m(1).values[0]
	xi = m(7).values[0]
	p11 = m(11).values[0]
	pn1 = m(1+s*11).values[0]
	pn2 = m(2+s*11).values[0]
	pn3 = m(3+s*11).values[0]
	print xi

	##fit with average xi
	hlp = little_help(n,r,p11,q)
	string = create_mokdxill(n,machine)
	m = Model(string)

	m.setPars({1+n*11:pn1,2+n*11:pn2,3+n*11:pn3})
	m(1+n*11).frozen = True
	m(2+n*11).frozen = True
	m(3+n*11).frozen = True
	for i in range(n):
		m.setPars({1+i*11:0,4+i*11:theta,5+i*11:phoindex,6+i*11:iron,7+i*11:xi,10+i*11:z,11+i*11:hlp[i]})
		m(4+i*11).frozen = True
		m(5+i*11).frozen = True
		m(6+i*11).frozen = True
		m(7+i*11).frozen = True
		m(8+i*11).frozen = True
		m(5+i*11).link = str(1+n*11)
		m(9+i*11).link = "4"
		m(10+i*11).frozen = True
		print i
		rin = 2+i*11
		rout = 3+i*11
		print rin, r[i][0]
		print rout, r[i][1]
		m.setPars({rin:r[i][0],rout:r[i][1]})

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "maximum 20,"
		for i in range(n):
			stringerr += str(11+i*11)+","
		stringerr = stringerr[:-1]
		Fit.error(stringerr)


	valS = []
	error = []
	x=[]
	testr=[]

	for i in range(n):
		valS.append(m(11+i*11).values[0]/S[i])
		x.append((r[i][0]+r[i][1])/2)
		error.append((m(11+i*11).error[0]+m(11+i*11).error[1])/2)
		testr.append((m(11+i*11).error[0]))

	return x,valS,error,testr


def fit_kdxill_var(n,index,iron,ionisation,z,absorption,norm,r,S,spin,theta,height,phoindex,err_fit):
	s=1
	string = create_mokdxill(s,machine)
	m = Model(string)


	m(1).frozen = False #don't care but better free
	m.setPars({1:0,4:theta,5:phoindex,6:iron,10:z})


	##free parameters index (1), ionization (8), norm(11)
	m.setPars({1:0,2:r[0][0],3:r[n-1][1]})
	m(9).link = "4"
	m(4).frozen = True
	m(5).frozen = True
	m(6).frozen = True
	m(7).frozen = False
	m(8).frozen = True
	m(11).frozen = False
	m.setPars({1+s*11:phoindex,2+s*11:1,3+s*11:1})
	m(5).link = "12"
	m(12).frozen = False

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	q = m(1).values[0]
	xi = m(7).values[0]
	p11 = m(11).values[0]

	pn1 = m(1+s*11).values[0]
	pn2 = m(2+s*11).values[0]
	pn3 = m(3+s*11).values[0]
	print xi

	xi = ionisation_profile_xillver(n,r)
	print xi

	##fit with average xi
	hlp = little_help(n,r,p11,q)
	print hlp
	string = create_mokdxill(n,machine)
	m = Model(string)

	m.setPars({1+n*11:pn1,2+n*11:pn2,3+n*11:pn3})
	m(1+n*11).frozen = True
	m(2+n*11).frozen = True
	m(3+n*11).frozen = True
	for i in range(n):
		m.setPars({1+i*11:0,4+i*11:theta,6+i*11:iron,7+i*11:xi[i],10+i*11:z,11+i*11:hlp[i]})
		m(4+i*11).frozen = True
		m(5+i*11).frozen = True
		m(6+i*11).frozen = True
		m(7+i*11).frozen = True
		m(8+i*11).frozen = True
		m(9+i*11).link = "4"
		m(5+i*11).link = str(1+n*11)
		m(10+i*11).frozen = True
		print i
		rin = 2+i*11
		rout = 3+i*11
		print rin, r[i][0]
		print rout, r[i][1]
		m.setPars({rin:r[i][0],rout:r[i][1]})




	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "maximum 20,"
		for i in range(n):
			stringerr += str(11+i*11)+","
		stringerr = stringerr[:-1]
		Fit.error(stringerr)


	valS = []
	error = []
	x=[]
	testr=[]

	for i in range(n):
		valS.append(m(11+i*11).values[0]/S[i])
		x.append((r[i][0]+r[i][1])/2)
		error.append((m(11+i*11).error[0]+m(11+i*11).error[1])/2)
		testr.append((m(11+i*11).error[0]))

	return x,valS,error,testr





#############################################publication testing end###################################################


def fit_kdrelavg_v2(n,index,iron,ionisation,z,absorption,norm,r,S,spin,theta,height,phoindex,err_fit):
	s=1
	string = create_mokdref(s,machine)
	m = Model(string)

	m.setPars({4:theta,5:iron,6:phoindex,7:ionisation,8:z})
	m(1).frozen = False
	m.setPars({2:r[0][0],3:r[n-1][1]})
	m(4).frozen = True
	m(5).frozen = True
	m(6).link = str(1+s*9)
	m(7).frozen = False
	m(8).frozen = True
	m(9).frozen = False
	m.setPars({1+s*9:phoindex,2+s*9:1e-3,3+s*9:1})
	m(10).frozen = False
	m(11).frozen = False
	m(12).frozen = False

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()
	print r
	q = m(1).values[0]
	avgxi = m(7).values[0]
	p4 = m(4).values[0]
	p9 = m(9).values[0]
	p5 = m(5).values[0]
	pn1 = m(1+s*9).values[0]
	pn2 = m(2+s*9).values[0]
	pn3 = m(3+s*9).values[0]
	print avgxi

	##fit with average xi
	hlp = little_help(n,r,p9,q)

	string = create_mokdref(n,machine)
	m = Model(string)

	m.setPars({1+n*9:pn1,2+n*9:pn2,3+n*9:pn3})
	m(1+n*9).frozen = True
	m(2+n*9).frozen = True
	m(3+n*9).frozen = True

	for i in range(n):
		m.setPars({1+i*9:0,4+i*9:theta,5+i*9:p5,7+i*9:ionisation,8+i*9:z,9+i*9:hlp[i]})
		m(4+i*9).frozen = True
		m(5+i*9).frozen = True
		m(6+i*9).frozen = True
		m(6+i*9).link = str(1+n*9)
		m(7+i*9).frozen = True

		print i
		rin = 2+i*9
		rout = 3+i*9
		print rin, r[i][0]
		print rout, r[i][1]
		m.setPars({rin:r[i][0],rout:r[i][1]})

	


	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "maximum 20,"
		for i in range(n):
			stringerr += str(9+i*9)+","
		stringerr = stringerr[:-1]
		Fit.error(stringerr)


	valS = []
	error = []
	x=[]

	print m(9).error

	for i in range(n):
		valS.append(m(9+i*9).values[0]/S[i])
		x.append((r[i][0]+r[i][1])/2)
		error.append(abs(m(9+i*9).error[0]-m(9+i*9).values[0]))

	print m(9).error
	return x,valS,error


# function takes closest ionisation value for distance x[i] calculated from average of boundries.. upgratable by fitting ionisation profile and take precise value
def takeClosest(myList, myNumber):
	closest = myList[0][0]
	testarg=[]
	for i in range(len(myList)):
		testarg.append(abs(myList[i][0] - myNumber)) 
	testarg = np.asarray(testarg)
	arg = testarg.argmin()
	return arg

def ionisation_profile(n,r):
	data = np.loadtxt("ionisation_00.dat") 
	x=[]
	for i in range(n):
		x.append((r[i][0]+r[i][1])/2)
	xi=[]
	for i in range(n):
		arg = takeClosest(data, x[i])
		if data[arg][1]>10:
			xi.append(data[arg][1])
		else: xi.append(10)
	return xi

def ionisation_profile_xillver(n,r):
	data = np.loadtxt("ionisation_00.dat") 
	x=[]
	for i in range(n):
		x.append((r[i][0]+r[i][1])/2)
	xi=[]
	for i in range(n):
		arg = takeClosest(data, x[i])
		if np.log10(data[arg][1])>0:
			xi.append(np.log10(data[arg][1]))
		elif np.log10(data[arg][1])<0: 
			xi.append(0)
	return xi




def fit_kdrelavgvar_v2(n,index,iron,ionisation,z,absorption,norm,r,S,spin,theta,height,phoindex,err_fit):
	s=1
	string = create_mokdref(s,machine)
	m = Model(string)

	m.setPars({4:theta,5:iron,6:phoindex,7:ionisation,8:z})
	m(1).frozen = False
	m.setPars({2:r[0][0],3:r[n-1][1]})
	m(4).frozen = True
	m(5).frozen = True
	m(6).link = str(1+s*9)
	m(7).frozen = False
	m(8).frozen = True
	m(9).frozen = False
	m.setPars({1+s*9:phoindex,2+s*9:1,3+s*9:1})
	m(10).frozen = False
	m(11).frozen = False
	m(12).frozen = False

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()
	print r
	q = m(1).values[0]
	avgxi = m(7).values[0]
	p5 = m(5).values[0]
	p4 = m(4).values[0]
	p9 = m(9).values[0]
	pn1 = m(1+s*9).values[0]
	pn2 = m(2+s*9).values[0]
	pn3 = m(3+s*9).values[0]


	##fit with average xi
	hlp = little_help(n,r,p9,q)
	xi = ionisation_profile(n,r)
	print xi

	string = create_mokdref(n,machine)
	m = Model(string)

	m.setPars({1+n*9:pn1,2+n*9:pn2,3+n*9:pn3})
	m(1+n*9).frozen = True
	m(2+n*9).frozen = True
	m(3+n*9).frozen = True

	for i in range(n):
		m.setPars({1+i*9:0,4+i*9:theta,5+i*9:p5,7+i*9:xi[i],8+i*9:z,9+i*9:hlp[i]})
		m(4+i*9).frozen = True
		m(5+i*9).frozen = True
		m(6+i*9).frozen = True
		m(6+i*9).link = str(1+n*9)
		m(7+i*9).frozen = True

		print i
		rin = 2+i*9
		rout = 3+i*9
		print rin, r[i][0]
		print rout, r[i][1]
		m.setPars({rin:r[i][0],rout:r[i][1]})


	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "maximum 20,"
		for i in range(n):
			stringerr += str(9+i*9)+","
		stringerr = stringerr[:-1]
		Fit.error(stringerr)


	valS = []
	error = []
	x=[]


	for i in range(n):
		valS.append((m(9+i*9).values[0]*xi[i])/(S[i]*avgxi))
		x.append((r[i][0]+r[i][1])/2+0.03*(r[i][0]+r[i][1])/2)
		error.append(abs(m(9+i*9).error[0]-m(9+i*9).values[0]))

	print m(9).error
	return x,valS,error

def create_mokdxill(n,machine):
	if machine == "home": string = "kdblur*atable{/mnt/31660B856FD2FABA/xspec/models/xillver/xillver-a-Ec2.fits}+"
	if machine == "elp": string = "kdblur*atable{/home/domcek/xspec/models/xillver/xillver-a-Ec2.fits}+"
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

def kdblur2_reflionx(n,index,iron,ionisation,z,absorption,norm,r,S,spin,theta,height,phoindex,err_fit):
	s=1
	string = create_mokdref(s,machine)
	m = Model(string)
	print r
	m.setPars({4:theta,5:iron,6:phoindex,7:ionisation,8:z,11:1e-3})
	m(1).frozen = False
	m.setPars({2:r[0][0],3:r[n-1][1]})
	m(4).frozen = True
	m(5).frozen = False
	m(6).link = str(1+s*9)
	m(7).frozen = False
	m(8).frozen = True
	m(9).frozen = False
	m.setPars({1+s*9:phoindex,2+s*9:1,3+s*9:1})
	m(10).frozen = False
	m(11).frozen = False
	m(12).frozen = False

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()
	print r
	q = m(1).values[0]
	avgxi = m(7).values[0]
	p5 = m(5).values[0]
	p4 = m(4).values[0]
	p9 = m(9).values[0]
	pn1 = m(1+s*9).values[0]
	pn2 = m(2+s*9).values[0]
	pn3 = m(3+s*9).values[0]

	m = Model("(kdblur2*atable{/mnt/31660B856FD2FABA/xspec/models/reflionx/reflionx.mod}+pow)*phabs")
	m.setPars({4:theta,7:p5,8:pn1,9:avgxi,10:z,11:p9,13:pn2,14:pn3})
	m(12).link = "8"
	m.setPars({2:r[0][0],3:r[n-1][1]})
	m(1).frozen = False

	m(4).frozen = True
	m(5).frozen = False
	m(6).frozen = False 
	m(7).frozen = True
	m(8).frozen = True
	m(9).frozen = True
	m(10).frozen = True
	m(11).frozen = True
	m(12).frozen = True
	m(13).frozen = True
	m(14).frozen = True

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()
	Fit.error("maximum 20, 1,5,6")

	Ix = m(1).values[0]
	Ix1 = m(6).values[0]
	Rbr = m(5).values[0]
	return Ix,Ix1,Rbr

####Create data####
def main(spin,theta,height,phoindex,index,iron,ionisation,z,absorption,norm,n,out,step1,start,finish,tables,err_fit):
	m = Model("kyreflionx*phabs")
	m.setPars({1:spin,2:theta,3:np.exp(start),5:np.exp(finish),7:height,8:phoindex,14:z,16:tables,18:1.5e-2})
	m.setPars({9:"-0.1 0.1 -10 -10 0 0"})

	fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=1e6)
	AllData.fakeit(1,fs,True,"fakeit_")
	AllModels.setEnergies(".1 10. 1000 log")
	AllData.ignore("**-1.0 10.0-**")
	AllData.show()
	
	AllModels.calcFlux("0.1 10")
	Fit.query = "yes"
	
	#Plot.setRebin("5","10")
	#Plot.xAxis = "keV"
	#Plot.device = "/xs"
	#Plot("ldata")

	r = create_r2(n,start,finish)
	S = create_S(r)

	print r
	
	Ix,Ix1,Rbr = kdblur2_reflionx(n,index,iron,ionisation,z,absorption,norm,r,S,spin,theta,height,phoindex,err_fit)

	x,ry,err_r = 0,0,0
	rx,ry,err_r = fit_kdrelavg_v2(n,index,iron,ionisation,z,absorption,norm,r,S,spin,theta,height,phoindex,err_fit)
	print err_r
	
	###Model kdblur+reflionx with changing xi
	rxvar,ryvar,err_rvar = 0,0,0
	rxvar,ryvar,err_rvar = fit_kdrelavgvar_v2(n,index,iron,ionisation,z,absorption,norm,r,S,spin,theta,height,phoindex,err_fit)
	print err_rvar

	#xxil,yxil,err_xil,testxil = fit_kdxill(n,index,iron,ionisation,z,absorption,norm,r,S,spin,theta,height,phoindex,err_fit)

	#xxil_v,yxil_v,err_xil_v,testxil_v = fit_kdxill_var(n,index,iron,ionisation,z,absorption,norm,r,S,spin,theta,height,phoindex,err_fit)
	
	print "Kdblur2*reflionx: Index", Ix,"Index1", Ix1, "Rbr", Rbr


	plot(rx,ry,".",color="red",label="kdblur+reflionx,xi=const")
	plot(rxvar,ryvar,".",color="black",label="kdblur+reflionx,xi=var")
	#plot(xxil,yxil,".",color="blue",label="kdblur+reflionx,xi=const")
	#plot(xxil_v,yxil_v,".",color="red",label="kdblur+reflionx,xi=const")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	ylim([10**(-22),10**4])
	#if len(rx) == len(err_r) : errorbar(rx ,ry, yerr = err_r, marker = "+", linestyle = "None") #weird stuff
	#if len(rxvar) == len(err_rvar) : errorbar(rxvar,ryvar, yerr = err_rvar, marker = "x", linestyle = "None") #weird stuff
	#if err_fit == True: errorbar(xxil,yxil, yerr = err_xil, marker = "None", linestyle = "None") #weird stuff
	#if err_fit == True: errorbar(xxil_v,yxil_v, yerr = err_xil_v, marker = "None", linestyle = "None") #weird stuff
	grid(True)
	legend()
	show()
	savefig("./play/compare_sp_"+str(spin)+"th_"+str(theta)+"h_"+str(height)+"phoi_"+str(phoindex)+"n_"+str(n)+"out_"+str(out)+"step1_"+str(step1)+"start_"+str(start)+".png")
	
	clf()
	

	f = open("./play/values_prague_sp_"+str(spin)+"th_"+str(theta)+"h_"+str(height)+"phoi_"+str(phoindex)+"n_"+str(n)+"out_"+str(out)+"step1_"+str(step1)+"start_"+str(start)+".txt",'w')
	#f.write("rx[i]" + 4*" " + "ry[i]" + 4*" " + "err_r[i]" + 4*" " + "kx[i]" + 4*" " + "ky[i]" + 4*" " + "err_k[i]" + "\n") 
	for i in range(len(rx)):
		f.write(str(rx[i]) + 4*" " + str(ry[i]) + 4*" " + str(err_r[i]) + 4*" " + str(rxvar[i]) + 4*" " + str(ryvar[i]) + 4*" " + str(err_rvar[i]) + "\n") 
	f.close()

	#f = open("./play/values_nowprague.txt",'w')
	#for i in range(len(rx)):
	#	f.write(str(rx[i]) + 4*" " + str(ry[i]) + 4*" " + str(rxvar[i]) + 4*" " + str(ryvar[i]) + "\n") 
	#f.close()
	return 0
	

machine = "home"

#AllModels.initpackage("kyreflionx", "lmodel.dat" ,"/mnt/31660B856FD2FABA/xspec/models/kyreflionx/ -udmget64")
if machine == "home":
	###Loaded models
	AllModels.lmod("kyreflionx","/mnt/31660B856FD2FABA/xspec/models/kyreflionx/")
	Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/kyreflionx/")
	AllModels.setEnergies(".1 50. 1000 log")
	
if machine == "elp":
	AllModels.lmod("kyreflionx","/home/domcek/xspec/models/kyreflionx/")
	Xset.addModelString("KYDIR","/home/domcek/xspec/models/kyreflionx/")
	AllModels.setEnergies(".1 50. 1000 log")

###
n=20
out = 1
step1 = 1
start = np.log(2.3) #start radius
finish = np.log(100) #end radius
###
spin = 0.9
theta = 55
height = 3
phoindex = 2.5
err_fit = False
iron = 8.88
ionisation = 53.44
z = 4.1e-2
norm = 1.5e-3
absorption = 1
index = 2 #index of emissivity
tables = 2 

main(spin,theta,height,phoindex,index,iron,ionisation,z,absorption,norm,n,out,step1,start,finish,tables,err_fit)

#pub(spin,theta,height,phoindex,index,iron,ionisation,z,absorption,norm,n,out,step1,start,finish,err_fit)