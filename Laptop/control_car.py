import pygame
import serial
from pygame.locals import *


#initialise 
pygame.init()
ser = serial.Serial('/dev/ttyUSB0', 11520, timeout=1)
repeat = True

def steer():
	while repeat:
		for event in pygame.event.get():
			if event.type == pygame.key.get_pressed():
				Key_input = pygame.key.get_pressed()

				#simple commands
				if Key_input[pygame.K_UP]:
					print 'Moving straight'
					ser.write(49)
				elif Key_input[pygame.K_DOWN]:
					print 'Moving reverse'
					ser.write(50)
				elif Key_input[pygame.K_LEFT]:
					print 'Moving left'
					ser.write(51)
				elif Key_input[pygame.K_RIGHT]:
					print 'Moving right'
					ser.write(52)

				#combination of commands
				elif Key_input[pygame.K_UP] and Key_input[pygame.K_RIGHT]:
					print 'Moving front and right'
					ser.write(53)
				elif Key_input[pygame.K_UP] and Key_input[pygame.K_LEFT]:
					print 'Moving front and left'
					ser.write(54)
				elif Key_input[pygame.K_DOWN] and Key_input[pygame.K_RIGHT]:
					print 'Moving back and right'
					ser.write(55)
				elif Key_input[pygame.K_DOWN] and Key_input[pygame.K_LEFT]:
					print 'Moving back and left'
					ser.write(56)

				#Quit 
				elif Key_input[pygame.K_x] or Key_input[pygame.K_q]:
					print 'Exiting!!'
					repeat = False
					ser.close()
					break
					
			#no key pressed??
			elif event.type == pygame.KEYUP:
				ser.write(48)


#call the function
steer()

