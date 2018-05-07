# This code is the final version
# for serial communication between
# arduino and laptop
import time
import datetime
import serial
import matplotlib.pyplot as plt
import numpy as np
import random
import sys
from scipy.signal import butter, lfilter, freqs
import scipy.fftpack 
from sklearn.externals import joblib


def butter_lowpass(fc, fs, order=5):
		b, a = butter(order,2.0*fc/fs , btype='low')
		return b, a

def butter_highpass(fc,fs,order=4):
		b, a = butter(order, 2.0*fc/fs, btype='high')
		return b, a 

max_valid_read = 1023
#max_valid_read = 4095
#V_ref = 3.3 
V_ref = 5.0
fs = 300
fcl = 40
fch = 7
dt = 1.0/fs
bl, al = butter_lowpass(fcl,fs,4)
bh, ah = butter_highpass(fch,fs,8)
#pkl = joblib.load('lb.pkl')
#LEFT = pkl[0][0] 
#RIGHT = pkl[1][0]

#LEFT = []
#RIGHT = []

#Arduino serial connection
ser = serial.Serial(
	port = '/dev/ttyACM0',
	baudrate = 115200,
	)

print('Connect to Arduino..')
time.sleep(5)
ser.flush()
#initiate transmission
ser.write('1')



#initialization of plot
it,r,b1_l,b2_l,b1_r,b2_r,count = 0,0,0,0,0,0,0
t = np.linspace(0,1,fs)
sp = np.linspace(0,fs/2,fs/2)
lv = np.zeros((fs,1))
ls = np.zeros((fs/2,1))
rv = np.zeros((fs,1))
rs = np.zeros((fs/2,1))

fig, axes = plt.subplots(nrows=2,ncols=2, sharex=False, sharey=False)
fig.suptitle('EEG signals')
linelv, = axes[0,0].plot(t, lv,'r-')
linels, = axes[1,0].plot(sp, ls, 'b-')
linerv, = axes[0,1].plot(t, rv, 'r-')
liners, = axes[1,1].plot(sp, rs, 'b-')

axes[0,0].set_xlim(0,1)
axes[0,0].set_ylim(-0.5,0.5)
axes[0,1].set_xlim(0,1)
axes[0,1].set_ylim(-0.5,0.5)
axes[1,0].set_ylim(0,6)
axes[1,1].set_ylim(0,6)
axes[0,0].set_title('Left Channel')
axes[0,1].set_title('Right Channel')
axes[0,0].set_xlabel('time(s)')
axes[1,0].set_xlabel('frequency(Hz)')
axes[1,0].set_title('Left Spectrum')
axes[1,1].set_title('Right Spectrum')
axes[0,0].set_ylabel('voltage(V)')
axes[1,0].set_ylabel('Amplitude')
plt.ion()



while True:
	try:
		while it < fs:
			b1_l = ord(ser.read(1))
			b2_l = ord(ser.read(1))
			r = b1_l + b2_l * 256
			r = (r * V_ref) / max_valid_read 
			lv[it,0] = r
			
			b1_r = ord(ser.read(1))
			b2_r = ord(ser.read(1))
			r = b1_r + b2_r * 256
			r = (r * V_ref) / max_valid_read 
			rv[it,0] = r
		
			it = it + 1
		dc1 = np.mean(lv)
		dc2 = np.mean(rv)
		lv -= dc1
		rv -= dc2

		#filtering
		left_f = lfilter(bh,ah,lv[:,0])
		fft_l = np.abs(np.fft.fft(left_f))
		right_f = lfilter(bh,ah,rv[:,0])
		fft_r = np.abs(np.fft.fft(right_f))

		#update plot
		linelv.set_ydata(left_f)
		linels.set_ydata(fft_l[:fs/2])
		linerv.set_ydata(right_f)
		liners.set_ydata(fft_r[:fs/2])

		plt.pause(0.1)
		it = 0

		"""			
		#manually filtering out bad data
		rcv = input('1:save; 2:skip; 3:quit    ')
		if rcv == '':
				raise KeyboardInterrupt
		if rcv == 1:
			count += 1
			print(count)	
			LEFT += [left_f] 
			RIGHT += [right_f]
		elif rcv == 2:
			print('pass')
		else:
			raise KeyboardInterrupt	
		"""
			
			
			
		ser.flush()
		ser.write('1')
	except KeyboardInterrupt:
		ser.close()
		plt.close()
		#pkl = [[LEFT], [RIGHT]]
		#joblib.dump(pkl, 'rb.pkl')
		sys.exit(1)

plt.ioff()
plt.show()
