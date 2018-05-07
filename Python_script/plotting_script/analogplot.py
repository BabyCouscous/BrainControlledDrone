import pyfirmata
import sys, serial
import datetime
import numpy as np
from time import sleep
from collections import deque
from matplotlib import pyplot as plt
from matplotlib import animation 

# class that holds analog data for N samples
class AnalogPlot:
	# constr
	def __init__(self, board, pin, maxLen):
		self.ax = deque([0.0]*maxLen)
		self.maxLen = maxLen
		self.pin = pin
		self.board = board

	# ring buffer
	def addToBuf(self, buf, val):
		if len(buf) < self.maxLen:
			buf.append(val)
		else:
			buf.pop()
			buf.appendleft(val)

	# add data
	def add(self, data):
		self.addToBuf(self.ax, data)

	# update plot
	def update(self, framenum, a0):
		try:
			data = self.pin.read()
			self.board.pass_time(dt)
			data = data * V_ref - 2.5
			self.add(data)
			a0.set_data(range(self.maxLen), self.ax)
		except KeyboardInterrupt:
			self.board.exit()	

		return a0


port = '/dev/ttyACM0' 
board = pyfirmata.Arduino(port)
print ('Setting up the connection to the board..')

analog_0 = board.get_pin('a:0:i')
it = pyfirmata.util.Iterator(board)
it.start()
analog_0.enable_reporting()

sampling_rate = 500
dt = 1.0/sampling_rate
V_ref = 5.0

# plot parameters
analogPlot = AnalogPlot(board, analog_0, 100)

print ('plotting data...')

fig = plt.figure()
ax = plt.axes(xlim=(0,100), ylim=(-2.5, 2.5))
a0 = ax.plot([], [])
anim = animation.FuncAnimation(fig, analogPlot.update, fargs=a0, interval=10)

plt.show()


