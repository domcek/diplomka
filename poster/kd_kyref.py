#!/usr/bin/python
from xspec import *
from pylab import *
import numpy as np


def main(spin,theta,height,phoindex,n,out,step1,start,finish,tables,err_fit):
	m = Model("kyreflionx*phabs")
	m.setPars({1:spin,2:theta,3:np.exp(start),5:np.exp(finish),7:height,8:phoindex,16:tables,18:1.5e-5})
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

	r = create_r(n,out,start,finish,step1)
	S = create_S(r)

	
	rx,ry,err_r,testr = 0,0,0,0
	rx,ry,err_r,testr = fit_kdrelavg_v2(n,r,S,spin,theta,height,phoindex,err_fit)
	
	###Model kdblur+reflionx with changing xi
	rxvar,ryvar,err_rvar,testrv = 0,0,0,0
	rxvar,ryvar,err_rvar,testrv = fit_kdrelavgvar_v2(n,r,S,spin,theta,height,phoindex,err_fit)
	
	print err_r

	plot(rx,ry,".",color="red",label="kdblur+reflionx,xi=const")
	plot(rxvar,ryvar,".",color="black",label="kdblur+reflionx,xi=var")
	xlabel("rg")
	ylabel("N(r)")
	xscale('log')
	yscale('log')
	ylim([10**(-22),10**4])
	if err_fit == True: errorbar(rx ,ry, yerr = err_r, marker = "None", linestyle = "None") #weird stuff
	if err_fit == True: errorbar(rxvar,ryvar, yerr = err_rvar, marker = "None", linestyle = "None") #weird stuff
	grid(True)
	legend()
	savefig("./play/compare_sp_"+str(spin)+"th_"+str(theta)+"h_"+str(height)+"phoi_"+str(phoindex)+"n_"+str(n)+"out_"+str(out)+"step1_"+str(step1)+"start_"+str(start)+".png")
	show()
	clf()
	

	f = open("./play/values_prague_sp_"+str(spin)+"th_"+str(theta)+"h_"+str(height)+"phoi_"+str(phoindex)+"n_"+str(n)+"out_"+str(out)+"step1_"+str(step1)+"start_"+str(start)+".txt",'w')
	#f.write("rx[i]" + 4*" " + "ry[i]" + 4*" " + "err_r[i]" + 4*" " + "kx[i]" + 4*" " + "ky[i]" + 4*" " + "err_k[i]" + "\n") 
	for i in range(len(rx)):
		f.write(str(rx[i]) + 4*" " + str(ry[i]) + 4*" " + str(err_r[i]) + 4*" " + str(rxvar[i]) + 4*" " + str(ryvar[i]) + 4*" " + str(err_rvar[i]) + 4*" " + str(testr[i])+ 4*" " + str(testrv[i]) + "\n") 
	f.close()

	f = open("./play/values_nowprague.txt",'w')
	for i in range(len(rx)):
		f.write(str(rx[i]) + 4*" " + str(ry[i]) + 4*" " + str(rxvar[i]) + 4*" " + str(ryvar[i]) + "\n") 
	f.close()
	return 0