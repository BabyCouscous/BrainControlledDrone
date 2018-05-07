from sklearn.externals import joblib 
import matplotlib.pyplot as plt
import numpy as np
import sys


fs = 300
dt = 1.0/fs
filename = raw_input('input file name: ')
#filename = 'blink_bb.pkl'
pkl = joblib.load(filename)

LEFT = pkl[0][0] 
RIGHT = pkl[1][0]

#pkl = [[LEFT],[RIGHT]]
#joblib.dump(pkl,'test.pkl')
print(len(LEFT))
print(len(RIGHT))

'''
t = np.linspace(0,1,fs)
fig, axes = plt.subplots(nrows=2,ncols=1, sharex=True, sharey=True)
axes[0].set_xlim(0,1)
axes[0].set_ylim(-0.5,0.5)
axes[1].set_xlabel('Time/(s)')
axes[0].set_ylabel('Volatge/(V)')
axes[1].set_ylabel('Voltage/(V)')
axes[0].plot(t,LEFT[17],'b-')
axes[0].set_title('Left Channel')
axes[1].plot(t,RIGHT[17],'b-')
axes[1].set_title('Right Channel')
plt.show()
'''


t = np.linspace(0,1,fs)
sp = np.linspace(0,fs/2,fs/2)
lv = np.zeros((fs,1))
ls = np.zeros((fs/2,1))
rv = np.zeros((fs,1))
rs = np.zeros((fs/2,1))

fig, axes = plt.subplots(nrows=2,ncols=1, sharex=False, sharey=False)
fig.suptitle('EEG signals')
linelv, = axes[0].plot(t, lv,'r-')
#linels, = axes[1,0].plot(sp, ls, 'b-')
linerv, = axes[1].plot(t, rv, 'r-')
#liners, = axes[1,1].plot(sp, rs, 'b-')
 
axes[0].set_xlim(0,1)
axes[0].set_ylim(-0.5,0.5)
axes[1].set_xlim(0,1)
axes[1].set_ylim(-0.5,0.5)
#axes[1,0].set_ylim(0,6)
#axes[1,1].set_ylim(0,6)
axes[0].set_title('Left Channel')
axes[1].set_title('Right Channel')
axes[0].set_xlabel('time(s)')
#axes[1,0].set_xlabel('frequency(Hz)')
#axes[1,0].set_title('Left Spectrum')
#axes[1,1].set_title('Right Spectrum')
axes[0].set_ylabel('voltage(V)')
#axes[1,0].set_ylabel('Amplitude')
plt.ion()


while True:
		index = input('enter index: ')
		if index == -1:
				sys.exit(1)	
		fft_l = np.abs(np.fft.fft(LEFT[index]))
		fft_r = np.abs(np.fft.fft(RIGHT[index]))

		#linels.set_ydata(fft_l[:fs/2])
		#liners.set_ydata(fft_r[:fs/2])
		linelv.set_ydata(LEFT[index])
		linerv.set_ydata(RIGHT[index])
		plt.pause(0.1)

plt.ioff()
plt.show()

