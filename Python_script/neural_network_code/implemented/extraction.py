import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
import sys


filename = raw_input('input file name: ')
pkl = joblib.load(filename + '.pkl')
LEFT = pkl[0][0]
RIGHT = pkl[1][0]

features = np.zeros((300,24))
ptr = 5

for i in xrange(300):
		fft_l = np.abs(np.fft.fft(LEFT[i]))
		fft_r = np.abs(np.fft.fft(RIGHT[i]))
		ptr = 5
		for j in xrange(12):
			features[i][j] = (fft_l[ptr-2] + fft_l[ptr-1] + fft_l[ptr] + fft_l[ptr+1] + fft_l[ptr+2])/5
			features[i][j+12] = (fft_r[ptr-2] + fft_r[ptr-1] + fft_r[ptr] + fft_r[ptr+1] + fft_r[ptr+2])/5
			ptr += 3

#joblib.dump(features,filename + '_ex.pkl')
#print(features[0:10,:])

pts = np.linspace(0,24,24)
fig, axes = plt.subplots(nrows=1, ncols=1)
line, = axes.plot(pts,features[0,:])
plt.ion()


while True:
		index = input('enter index: ')
		if index == -1:
				sys.exit(1)
		line.set_ydata(features[index,:])
		plt.pause(0.1)

plt.ioff()
plt.show()


