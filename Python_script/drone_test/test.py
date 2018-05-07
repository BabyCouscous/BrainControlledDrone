#########
# firstTry.py
# This program is part of the online PS-Drone-API-tutorial on www.playsheep.de/drone.
# It shows how to do basic movements with a Parrot AR.Drone 2.0 using the PS-Drone-API.
# Dependencies: a POSIX OS, PS-Drone-API 2.0 beta or higher.
# (w) J. Philipp de Graaff, www.playsheep.de, 2014
##########
# LICENCE:
#   Artistic License 2.0 as seen on http://opensource.org/licenses/artistic-license-2.0 (retrieved December 2014)
#   Visit www.playsheep.de/drone or see the PS-Drone-API-documentation for an abstract from the Artistic License 2.0.
###########

import time
import ps_drone                # Imports the PS-Drone-API
import sys
import fcntl
import termios
import os



fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO 
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

drone = ps_drone.Drone()       # Initializes the PS-Drone-API
drone.startup()                # Connects to the drone and starts subprocesses
drone.reset()

time.sleep(6)                # Gives the drone time to start


try:
		while 1:
				try:
						c = sys.stdin.read(1).lower()
						if c == 'q':
								print('break')
								break
						elif c == 'a':
								print('move left')
								drone.moveLeft()
						elif c == 'd':
								print('move right')
								drone.moveRight()
						elif c == 'w':
								print('move forward')
								drone.moveForward()
						elif c == 's':
								print('move backward')
								drone.moverBackward()
						elif c == ' ':
								print('take off')
								drone.takeoff()
								time.sleep(6)
						elif c == '\n':
								print('land')
								drone.land()
						elif c == 'r':
								print('reset')
								drone.reset()
						time.sleep(1)
						drone.stop()
				except:
						#termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
						#fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
						#drone.land()
						#drone.shutdown()
						pass
finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
		drone.land()
		drone.shutdown()
		print('done')
