#!/usr/bin/python

#before using script type into terminal:
"""
export HEADAS=/opt/heasoft-6.16/x86_64-unknown-linux-gnu-libc2.19-0/
alias heainit=". $HEADAS/headas-init.sh"
heainit
"""
from xspec import *
from pylab import *

AllModels.lmod("ky","/home/mecgyver/xspec/KY")
Xset.addModelString("KYDIR","/home/mecgyver/xspec/KY/")
Xset.show()

AllModels.setEnergies(".1 50. 1000 log")

m1 = Model("bbody", setPars=(2,1))

x1=m1.energies(0)
y1=m1.values(0)
x1.pop()

m2 = Model("bbody", setPars=(3,1))

x2=m2.energies(0)
y2=m2.values(0)
x2.pop()

m3 = Model("bbody", setPars=(5,1))

x3=m3.energies(0)
y3=m3.values(0)
x3.pop()

print y3

m4 = Model("kyrline")
x4=m4.energies(0)
y4=m4.values(0)
x4.pop()




# Create an array of 1000 logarithmic-spaced bins, from .1 to 50. keV
#  AllModels.setEnergies(".1 50. 1000 log")


f, ax = plt.subplots()
ax.plot(x1,y1, "r", label="kT = 2 keV")
ax.plot(x2,y2, "g", label="kT = 3 keV")
ax.plot(x3,y3, "b", label="kT = 5 keV")
#ax.plot(x4,y4, "y")
ax.grid(True)
ax.set_title('Blackbody model')
ax.set_xlabel("Energy [keV]")
ax.set_ylabel('Photons cm$^{-2}\cdot$s$^{-1}\cdot$keV$^{-1}$')
ax.set_xscale('log')
ax.set_yscale('log')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels,loc = "lower left")
savefig("plot.pdf")





def my_plotter(ax, data1, data2, param_dict):
    """
    A helper function to make a graph

    Parameters
    ----------
    ax : Axes
        The axes to draw to

    data1 : array
       The x data

    data2 : array
       The y data

    param_dict : dict
       Dictionary of kwargs to pass to ax.plot

    Returns
    -------
    out : list
        list of artists added
    """
    out = ax.plot(data1, data2, **param_dict)
    return out
