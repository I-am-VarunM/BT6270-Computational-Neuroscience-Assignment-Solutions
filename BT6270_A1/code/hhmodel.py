import sys
import numpy as np
from math import exp
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("whitegrid")

#PLotting Graph
def plotmygraph(I1, I2, I3,current_range, npeaks_hist):
	print("\nThe cutoff currents:")
	print("I1 =", I1, "\u03bcA/$mm^2$")
	print("I2 =", I2, "\u03bcA/$mm^2$")
	print("I3 =", I3, "\u03bcA/$mm^2$")
	plt.figure()
	plt.axvline(I1, color="y")
	plt.axvline(x=I2, color="y")
	plt.axvline(x=I3, color="y")
	plt.plot(current_range, npeaks_hist)
	plt.title("Frequency of Spiking vs Input Current")
	plt.xlabel("Input Current (\u03bcA/$mm^2$)")
	plt.ylabel("Frequency of Spiking")
	plt.show()
	
	
current_range = np.arange(0, 0.6, 0.001)
npeaks_hist = np.zeros(current_range.shape)

for cur_iter in tqdm(range(current_range.size)):
	#Deifning constants
	gkmax = 0.36
	vk = -77
	gnamax = 1.20
	vna = 50
	gl = 0.003
	vl = -54.387
	cm = 0.01

	dt = 0.01#increase it for faster inference but less accurate one
	niter = 50000
	t = np.arange(1, niter, dt)

	v = -64.9964
	m = 0.0530
	h = 0.5960
	n = 0.3177

	gnahist = np.zeros((niter))
	gkhist = np.zeros((niter))
	vhist = np.zeros((niter))
	mhist = np.zeros((niter))
	hhist = np.zeros((niter))
	nhist = np.zeros((niter))

#Calculating values for different time stamps
	for iteration in range(niter):
		#Defining constants
		gna = gnamax*m**3*h
		gk = gkmax*n**4
		vinf = ((gna*vna+gk*vk+gl*vl) + current_range[cur_iter])/(gna + gk + gl)
		tauv = cm/(gna + gk + gl)

		v = vinf+(v-vinf)*exp(-dt/tauv)

		alpham = 0.1*(v+40)/(1-exp(-(v+40)/10))
		betam = 4*exp(-0.0556*(v+65))

		alphan = 0.01*(v+55)/(1-exp(-(v+55)/10))
		betan = 0.125*exp(-(v+65)/80)

		alphah = 0.07*exp(-0.05*(v+65))
		betah = 1/(1+exp(-0.1*(v+35)))

		taum = 1/(alpham+betam)
		tauh = 1/(alphah+betah)
		taun = 1/(alphan+betan)

		minf = alpham*taum
		hinf = alphah*tauh
		ninf = alphan*taun

		m = minf+(m-minf)*exp(-dt/taum)
		h = hinf+(h-hinf)*exp(-dt/tauh)
		n = ninf+(n-ninf)*exp(-dt/taun)
#Assigning values
		vhist[iteration] = v
		mhist[iteration] = m
		hhist[iteration] = h
		nhist[iteration] = n
	threshold = 5
	npeaks = 0
	for i in range(vhist.size-1):
		if (vhist[i] >= threshold) and (vhist[i] > vhist[i+1]) and (vhist[i] > vhist[i-1]):
			npeaks += 1
	#npeaks = find_peaks(vhist)
	npeaks_hist[cur_iter] = npeaks
#Finding the values of I1, I2 and I3
for i in range(npeaks_hist.size-1):
	if npeaks_hist[i] > 0 and npeaks_hist[i-1] == 0:
			I1 = i
	if npeaks_hist[i+1]-npeaks_hist[i] > 3: #Assumption point no 3 in report
			I2 = i
	if npeaks_hist[i+1]-npeaks_hist[i] < -7: #Assumption point no 4 in report
			I3 = i
plotmygraph(current_range[I1], current_range[I2], current_range[I3], current_range, npeaks_hist)