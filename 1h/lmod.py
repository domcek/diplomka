#!/usr/bin/python
from xspec import *
from pylab import *

AllModels.lmod("reflionx","/mnt/31660B856FD2FABA/xspec/models/reflionx/")
m = Model("reflionx")