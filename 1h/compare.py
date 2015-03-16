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

def create_S(r):
	S = []
	for i in range(len(r)):
		Sm = 2*np.pi*(r[i][1]-r[i][0])
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
	new_string = ""
	for i in range(n):
		new_string += string 
		if i == (n-1):
			new_string = new_string[:-1] 
	return new_string

def fit_kyreflionx(n,r,S,spin,theta,height,phoindex,err_fit):
	s=1
	string = create_mokyx(s)
	m = Model(string)

	m.setPars({(1):spin,(2):theta,(7):height,(8):phoindex})
	m.setPars({(9):"-0.1 0.1 -10 -10 0 0"})

	m.setPars({3:r[0][0],5:100})
	m(3).frozen = True
	m(5).frozen = True
	m(9).frozen = True
	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	p1 = m(1).values[0]
	p2 = m(2).values[0]
	p4 = m(4).values[0]
	p6 = m(6).values[0]
	p7 = m(7).values[0]
	p8 = m(8).values[0]
	p10 = m(10).values[0]
	p11 = m(11).values[0]
	p12 = m(12).values[0]
	p13 = m(13).values[0]
	p14 = m(14).values[0]
	p15 = m(15).values[0]
	p16 = m(16).values[0]
	p17 = m(17).values[0]
	p18 = m(18).values[0]

	

	string = create_mokyx(n)
	m = Model(string)

	for i in range(n):
		m.setPars({(1+i*18):p1,(2+i*18):p2,(7+i*18):p7,(8+i*18):p8})
		m.setPars({(4+i*18):p4,(6+i*18):p6,(10+i*18):p10,(11+i*18):p11,(12+i*18):p12,(13+i*18):p13,(14+i*18):p14,(15+i*18):p15,(16+i*18):p16,(17+i*18):p17,(18+i*18):p18})
		m.setPars({(9):"-0.1 0.1 -10 -10 0 0"})
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
		print r[i][0], "-", r[i][1]
		m.setPars({rin:r[i][0],rout:r[i][1]})

	""" #functional
	for i in range(n):
		m.setPars({(1+i*18):spin,(2+i*18):theta,(7+i*18):height,(8+i*18):phoindex})
		m.setPars({(4+i*18):p4,(6+i*18):p6,(10+i*18):p10,(11+i*18):p11,(12+i*18):p12,(13+i*18):p13,(14+i*18):p14,(15+i*18):p15,(16+i*18):p16,(17+i*18):p17,(18+i*18):p18})
		m.setPars({(9+i*18):"-0.1 0.1 -10 -10 0 0"})
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
		print r[i][0], "-", r[i][1]
		m.setPars({rin:r[i][0],rout:r[i][1]})
	"""
	AllModels.show()

	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True: 
		stringerr = "stop 10 0.01,maximum 1500.0"
		for i in range(n):
			stringerr += ","+str(18+i*18)
		Fit.error(stringerr)

	##Surface Norm
	valS = []
	error = []
	x=[]
	for i in range(n):
		valS.append(m(18+i*18).values[0]/S[i])
		error.append((m(18+i*18).error[0]+m(18+i*18).error[1])/2)
		x.append((r[i][0]+r[i][1])/2)
	"""
	plot(x,valS,".")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	errorbar(x ,value, yerr = error, marker = "None", linestyle = "None") #weird stuff
	grid(True)
	savefig("kyreflionx_surfnorm_spin"+str(spin)+".pdf")
	"""
	return x,valS,error

def fit_kyreflionx_only1(n,spin,theta,height,phoindex,err_fit,start,finish):
	string = create_mokyx(n)
	m = Model(string)


	m(1).frozen = True
	m(2).frozen = True
	m(6).frozen = True
	m(7).frozen = True
	m(8).frozen = True
	m(9).frozen = True
	m(10).frozen = True
	m(11).frozen = True
	m(12).frozen = True
	m(13).frozen = True
	m.setPars({(1):spin,(2):theta,(7):height,(8):phoindex})
	m.setPars({3:np.exp(start),5:np.exp(finish)})
	m.setPars({9:"-0.1 0.1 -10 -10 0 0"})

	AllModels.show()

	Fit.nIterations = 10000
	Fit.perform()
	return 0

def fit_kdrelavg(n,r,S,spin,theta,height,phoindex,err_fit):
	s=1
	string = create_mokdref(s,machine)
	m = Model(string)

	m(4).frozen = True
	m(5).frozen = True
	m(6).frozen = True
	m(9).frozen = True

	Fit.nIterations = 10000
	Fit.perform()
	xi = m(7).values[0]
	print xi

	##fit with average xi

	string = create_mokdref(n,machine)
	m = Model(string)

	for i in range(n):
		m.setPars({1+i*9:0,(4+i*9):theta,(6+i*9):phoindex})
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
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "stop 10 20,maximum 300000.0"
		for i in range(n):
			stringerr += ","+str(9+i*9)
		Fit.error(stringerr)

	valS = []
	error = []
	x=[]

	for i in range(n):
		valS.append(m(9+i*9).values[0]/S[i])
		x.append((r[i][0]+r[i][1])/2)
		error.append((m(9+i*9).error[0]+m(9+i*9).error[1])/2)

	"""
	plot(x,valS,".")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	#errorbar(x ,value, yerr = error, marker = "None", linestyle = "None") #weird stuff
	grid(True)
	savefig("kdref_surfnorm_log.pdf")
	"""

	return x,valS,error

def fit_kdrelavg_v2(n,r,S,spin,theta,height,phoindex,err_fit):
	s=1
	string = create_mokdref(s,machine)
	m = Model(string)

	m(1).frozen = True
	m.setPars({2:r[0][0],3:r[n-1][1]})
	m(4).frozen = True
	m(5).frozen = False
	m(6).frozen = True
	m(9).frozen = False
	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	p5 = m(5).values[0]
	xi = m(7).values[0]
	p9 = m(9).values[0]
	print xi

	##fit with average xi

	string = create_mokdref(n,machine)
	m = Model(string)

	for i in range(n):
		m.setPars({1+i*9:0,4+i*9:theta,5+i*9:p5,6+i*9:phoindex,7+i*9:xi,9+i*9:p9})
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
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "stop 10 20,maximum 300000.0"
		for i in range(n):
			stringerr += ","+str(9+i*9)
		Fit.error(stringerr)

	valS = []
	error = []
	x=[]

	for i in range(n):
		valS.append(m(9+i*9).values[0]/S[i])
		x.append((r[i][0]+r[i][1])/2)
		error.append((m(9+i*9).error[0]+m(9+i*9).error[1])/2)

	"""
	plot(x,valS,".")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	#errorbar(x ,value, yerr = error, marker = "None", linestyle = "None") #weird stuff
	grid(True)
	savefig("kdref_surfnorm_log.pdf")
	"""

	return x,valS,error

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


def fit_kdrelavgvar(n,r,S,spin,theta,height,phoindex,err_fit):
	xi = ionisation_profile(n,r)

	string = create_mokdref(n,machine)
	m = Model(string)

	print xi
	for i in range(n):
		m.setPars({(4+i*9):theta,(6+i*9):phoindex})
		m(4+i*9).frozen = True
		m(5+i*9).frozen = True
		m(6+i*9).frozen = True
		m.setPars({(7+i*9):xi[i]})
		m(7+i*9).frozen = True

		print i
		print xi[i]
		rin = 2+i*9
		rout = 3+i*9
		print rin, r[i][0]
		print rout, r[i][1]
		m.setPars({rin:r[i][0],rout:r[i][1]})

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "stop 10 20,maximum 300000.0"
		for i in range(n):
			stringerr += ","+str(9+i*9)
		Fit.error(stringerr)

	valS = []
	error = []
	x=[]

	for i in range(n):
		valS.append(m(9+i*9).values[0]/S[i])
		x.append((r[i][0]+r[i][1])/2)
		error.append((m(9+i*9).error[0]+m(9+i*9).error[1])/2)

	"""
	plot(x,valS,".")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	#errorbar(x ,value, yerr = error, marker = "None", linestyle = "None") #weird stuff
	grid(True)
	savefig("kdref_surfnorm_log.pdf")
	"""

	return x,valS,error

def fit_kdrelavgvar_v2(n,r,S,spin,theta,height,phoindex,err_fit):
	s=1
	string = create_mokdref(s,machine)
	m = Model(string)

	m(1).frozen = True
	m.setPars({2:r[0][0],3:r[n-1][1]})
	m(4).frozen = True
	m(5).frozen = False
	m(6).frozen = True
	m(9).frozen = False
	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	p5 = m(5).values[0]
	p9 = m(9).values[0]


	xi = ionisation_profile(n,r)

	string = create_mokdref(n,machine)
	m = Model(string)

	print xi
	for i in range(n):
		m.setPars({1+i*9:0,4+i*9:theta,5+i*9:p5,6+i*9:phoindex,7+i*9:xi[i],9+i*9:p9})
		m(4+i*9).frozen = True
		m(5+i*9).frozen = True
		m(6+i*9).frozen = True
		m(7+i*9).frozen = True

		print i
		print xi[i]
		rin = 2+i*9
		rout = 3+i*9
		print rin, r[i][0]
		print rout, r[i][1]
		m.setPars({rin:r[i][0],rout:r[i][1]})

	AllModels.show()
	Fit.nIterations = 10000
	Fit.perform()

	if err_fit == True:
		stringerr = "stop 10 20,maximum 300000.0"
		for i in range(n):
			stringerr += ","+str(9+i*9)
		Fit.error(stringerr)

	valS = []
	error = []
	x=[]

	for i in range(n):
		valS.append(m(9+i*9).values[0]/S[i])
		x.append((r[i][0]+r[i][1])/2)
		error.append((m(9+i*9).error[0]+m(9+i*9).error[1])/2)

	"""
	plot(x,valS,".")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	#errorbar(x ,value, yerr = error, marker = "None", linestyle = "None") #weird stuff
	grid(True)
	savefig("kdref_surfnorm_log.pdf")
	"""

	return x,valS,error

### Fakedata model parameters of kyrefliuonx


def only1(spin,theta,height,phoindex,n,out,step1,start,finish,err_fit):
	m = Model("kyreflionx")
	m.setPars({1:spin,2:theta,3:np.exp(start),5:np.exp(finish),7:height,8:phoindex})
	m.setPars({9:"-0.1 0.1 -10 -10 0 0"})

	fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=2e5)
	AllData.fakeit(1,fs,False,"fakeit_")
	AllModels.setEnergies(".1 10. 1000 log")
	AllData.ignore("**-3.0 5.0-**")
	AllData.show()	

	s = fit_kyreflionx_only1(n,spin,theta,height,phoindex,err_fit,start,finish)

####Create data####
def main(spin,theta,height,phoindex,n,out,step1,start,finish,err_fit):
	m = Model("kyreflionx")
	m.setPars({1:spin,2:theta,3:np.exp(start),5:np.exp(finish),7:height,8:phoindex})
	m.setPars({9:"-0.1 0.1 -10 -10 0 0"})

	fs = FakeitSettings(response="epn_ff20_sdY9_v12.0.rmf",arf="pn-thin-5.arf",exposure=2e5)
	AllData.fakeit(1,fs,False,"fakeit_")
	AllModels.setEnergies(".1 10. 1000 log")
	AllData.ignore("**-1.0 10.0-**")
	AllData.show()

	Plot.setRebin("5","10")
	Plot.xAxis = "keV"
	Plot.device = "/xs"
	Plot("ldata")


	r = create_r(n,out,start,finish,step1)
	S = create_S(r)

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
		stringerr = "stopat 10000, maximum 1000, "
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

	###Model kdblur+reflionx
	#rx,ry,err_r = 0,0,0
	#rx,ry,err_r = fit_kdrelavg(n,r,S,spin,theta,height,phoindex,err_fit)

	rx,ry,err_r = 0,0,0
	rx,ry,err_r = fit_kdrelavg_v2(n,r,S,spin,theta,height,phoindex,err_fit)

	###Model kdblur+reflionx with changing xi
	rxvar,ryvar,err_rvar = 0,0,0
	rxvar,ryvar,err_rvar = fit_kdrelavgvar_v2(n,r,S,spin,theta,height,phoindex,err_fit)
	
	###Fit by kyreflionx
	#kx,ky,err_k = 0,0,0	
	#kx,ky,err_k = fit_kyreflionx(n,r,S,spin,theta,height,phoindex,err_fit)
	
	print r
	#plot(kx,ky,".",color="blue",label="kyreflionx")
	plot(rx,ry,".",color="red",label="kdblur+reflionx,xi=const")
	plot(rxvar,ryvar,".",color="black",label="kdblur+reflionx,xi=var")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	ylim([10**(-22),10**4])
	#if err_fit == True: errorbar(kx ,ky, yerr = err_k, marker = "None", linestyle = "None") #weird stuff
	#if err_fit == True: errorbar(rx ,ry, yerr = err_r, marker = "None", linestyle = "None") #weird stuff
	if err_fit == True: errorbar(rxvar,ryvar, yerr = err_rvar, marker = "None", linestyle = "None") #weird stuff
	grid(True)
	legend()
	savefig("./play/compare_sp_"+str(spin)+"th_"+str(theta)+"h_"+str(height)+"phoi_"+str(phoindex)+"n_"+str(n)+"out_"+str(out)+"step1_"+str(step1)+"start_"+str(start)+".png")
	show()
	clf()
	

	#f = open("values_sp_"+str(spin)+"th_"+str(theta)+"h_"+str(height)+"phoi_"+str(phoindex)+"n_"+str(n)+"out_"+str(out)+"step1_"+str(step1)+"start_"+str(start)+".txt",'w')
	#f.write("rx[i]" + 4*" " + "ry[i]" + 4*" " + "err_r[i]" + 4*" " + "kx[i]" + 4*" " + "ky[i]" + 4*" " + "err_k[i]" + "\n") 
	#for i in range(len(kx)):
	#	f.write(str(rx[i]) + 4*" " + str(ry[i]) + 4*" " + str(err_r[i]) + 4*" " + str(kx[i]) + 4*" " + str(ky[i]) + 4*" " + str(err_k[i]) + "\n") 
	#f.close()

	return 0


machine = "home"

if machine == "home":
	###Loaded models
	AllModels.lmod("kyreflionx","/mnt/31660B856FD2FABA/xspec/models/kyreflionx/")
	Xset.addModelString("KYDIR","/mnt/31660B856FD2FABA/xspec/models/kyreflionx/")
	AllModels.setEnergies(".1 50. 1000 log")
	#AllModels.initpackage("kyreflionx", "lmodel.dat" ,"/mnt/31660B856FD2FABA/xspec/models/kyreflionx/ -udmget64")
if machine == "elp":
	AllModels.lmod("kyreflionx","/home/domcek/xspec/models/kyreflionx/")
	Xset.addModelString("KYDIR","/home/domcek/xspec/models/kyreflionx/")
	AllModels.setEnergies(".1 50. 1000 log")

###
n=5
out = 1
step1 = 0.2
start = np.log(3) #start radius
finish = np.log(100) #end radius
###
spin = 0.7
theta = 55
height = 3
phoindex = 2
err_fit = False

main(spin,theta,height,phoindex,n,out,step1,start,finish,err_fit)
#only1(spin,theta,height,phoindex,n,out,step1,start,finish,err_fit)
