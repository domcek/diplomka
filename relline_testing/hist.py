import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("rel.txt")
k=0
for i in range(len(data)):
	if data[i]<3 or data[i]>6: k+=1
print k	


plt.hist(data, bins=50, color='blue')
plt.savefig("histogram.png")