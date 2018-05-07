# Read signals and process them,
# send command to the drone
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
import pyautogui
import ps_drone


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


NN = joblib.load('NN.pkl')
scaler = joblib.load('scaler.pkl')


p1 = np.zeros((1,4))
p2 = np.zeros((1,4))
p1[0][0] = 1
p2[0][0] = 1

drone_on = True 
#x, y = pyautogui.position()
#xmax, ymax = pyautogui.size()
#delta = 50

'''
t = np.zeros((1,4))
t[0][1] = 1
t[0][2] = 1
print(t.argmax(1))
'''



if drone_on:
	#start drone
	drone = ps_drone.Drone()
	drone.startup()
	drone.reset()
	print('Connect to Drone..')
	time.sleep(3)
	drone.takeoff()


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

		features = np.zeros((1,24))
		ptr = 5
		for j in xrange(12):
				features[0][j] = (fft_l[ptr-2] + fft_l[ptr-1] + fft_l[ptr] + fft_l[ptr+1] + fft_l[ptr+2])/5
				features[0][j+12] = (fft_r[ptr-2] + fft_r[ptr-1] + fft_r[ptr] + fft_r[ptr+1] + fft_r[ptr+2])/5	

		features = scaler.transform(features)
		prob = NN.predict_proba(features)

		predictions = np.zeros_like(prob)
		predictions[np.arange(len(prob)), prob.argmax(1)] = 1
		print(predictions)

		#res = (p1 + p2 + predictions)/3.0
		#print(res)

		#prob = NN.predict_proba(features)
		index = prob.argmax(1)

		#update
		#p2 = p1
		#p1 = predictions
	
		if drone_on:
				if index == 0:
						#stay
						time.sleep(0.5)
						#y -= delta
						#y = max(y,0)
				elif index == 1:
						#move forward 
						drone.moveForward(0.3)
						time.sleep(0.5)
						#y += delta
						#y = min(ymax,y)
				elif index == 2:
						#move left
						drone.turnLeft(0.5)
						time.sleep(0.5)
						#x -= delta
						#x = max(x,0)
				else:
						#move right
						drone.turnRight(0.3)
						time.sleep(0.5)
						#x += delta
						#x = min(x,xmax)
				drone.stop()
				time.sleep(0.5)

		#pyautogui.moveTo(x,y)
		#predictions = np.zeros_like(prob)
		#predictions[np.arange(len(prob)), prob.argmax(1)] = 1
		#print(predictions)


		it = 0

		ser.flush()
		ser.write('1')
	except KeyboardInterrupt:
		ser.close()
		if drone_on:
			drone.land()
			drone.shutdown()
		sys.exit(1)

