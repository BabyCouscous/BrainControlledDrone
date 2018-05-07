# This code is the final version
# for serial communication between
# arduino and laptop
import time
import datetime
import serial
import matplotlib.pyplot as plt
import numpy as np
import random

#max_valid_read = 1023
max_valid_read = 4095
V_ref = 3.3 
fs = 160
dt = 1.0/160


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
it,r,b1_l,b2_l,b1_r,b2_r = 0,0,0,0,0,0
t = np.linspace(0,1,fs)
left = np.zeros((160,1))
right = np.zeros((160,1))
fig, (ax1,ax2) = plt.subplots(nrows=2, sharex=True, sharey=True)
fig.suptitle('EEG signals')
line1, = ax1.plot(t,left,'r-')
line2, = ax2.plot(t,right, 'b-')
ax1.set_xlim(0,1)
ax1.set_ylim(-0.2,0.2)
ax1.set_title('Left Channel')
ax2.set_xlabel('time(s)')
ax2.set_title('Right Channel')
ax1.set_ylabel('voltage(V)')
ax2.set_ylabel('voltage(V)')
plt.ion()

while True:
	try:
		while it < fs:
			b1_l = ord(ser.read(1))
			#print('read')
			b2_l = ord(ser.read(1))
			r = b1_l + b2_l * 256
			r = (r * V_ref)/max_valid_read 
			left[it,0] = r

			b1_r = ord(ser.read(1))
			b2_r = ord(ser.read(1))
			r = b1_r + b2_r * 256
			r = (r* V_ref)/max_valid_read 
			right[it,0] = r

			it = it + 1
		dc1 = np.mean(left)
		dc2 = np.mean(right)
		#left = left - V_ref/2 
		#right = right - V_ref/2 
		left = left - dc1
		right = right - dc2
		#print('finished reading')
		line1.set_ydata(left)
		line2.set_ydata(right)
		#tic = datetime.datetime.now()
		plt.pause(0.1)
		#toc = datetime.datetime.now()
		#delta = toc - tic
		#print(delta.microseconds)
		it = 0
		ser.flush()
		ser.write('1')
	except KeyboardInterrupt:
		ser.close()
		fig.close()
		pass

plt.ioff()
plt.show()
