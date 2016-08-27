import pygame
import serial
from pygame.locals import *
import time

#initialise
print 'starting pygame...'
screen = pygame.display.set_mode((400, 300))
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

#let's steer!!
def steer():
	repeat = True
	while repeat:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				key_input = pygame.key.get_pressed()
				
				#simple commands
				if key_input[pygame.K_UP]:
					print 'moving forward...'
					ser.write(chr(49))
				if key_input[pygame.K_DOWN]:
					print 'moving back...'
					ser.write(chr(50))
				if key_input[pygame.K_LEFT]:
					print 'moving left...'	
					ser.write(chr(51))
				if key_input[pygame.K_RIGHT]:
					print 'moving right...'
					ser.write(chr(52))
				

				#quit
				if key_input[pygame.K_q]:
					print 'quit...'	
					repeat = False
			
				
				#combination of commands
				if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
					print 'moving front right...'
					ser.write(chr(53))
				if key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
					print 'moving front left...'
					ser.write(chr(54))
				if key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
					print 'moving back right...'
					ser.write(chr(55))
				if key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
					print 'moving back left...'		
					ser.write(chr(56))



		#update the screen 
		pygame.display.flip()
	print 'done!!...'
	ser.close()
print 'starting steer...'
time.sleep(2)
steer()
