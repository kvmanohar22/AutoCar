import cv2
import serial
import numpy as np
import io 
import socket
import struct
import time
import pygame
from pygame.locals import *


host = '0.0.0.0'
port = 2222

server_socket = socket.socket()
server_socket.bind((host, port))

print 'I am listening to the incoming connections...'
server_socket.listen(0)
connection = server_socket.accept()[0].makefile('rb')

#initialise some variables
input_data = np.zeros((1, 38400))
output_labels = np.zeros((4, 4)).astype(np.float32)
for i in xrange(4):
	output_labels[i, i] = 1

print 'Shape of input data: ', input_data.shape
print 'Shape of output labels: ', output_labels.shape

print 'Initialising pygame...'
pygame.init()

print 'Opening serial port...'
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

frame = 1

print 'Starting timer...'
start = time.time()

#start collecting the images
try:
	while True:

		#read a single frame from the camera
		image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
		if not image_len:
			break

		image_stream = io.BytesIO()
		image_stream.write(connection.read(image_len))

		image_stream.seek(0)
		img_array = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
		image = cv2.imdecode(img_array, 0)

		#select lower half of the image
		temp_image_mat = image[120:240, :]
		temp_image_arr = temp_image_mat.reshape((1, 38400))

		print 'Collected image #', frame
		input_data = np.vstack((input_data, temp_image_arr))

		#show some details of the image
		cv2.imwrite('frame{:>05}.jpg'.format(frame), image)
		frame += 1
		cv2.imshow('input image', image)

		cv2.waitKey(1) & 0xFF


		#read the corresponding input from the human driver
		for event in pygame.event.get():
			if event.type == pygame.key.get_pressed():
				Key_input = pygame.key.get_pressed()

				#simple commands
				if Key_input[pygame.K_UP]:
					ser.write(49)
					temp_label = output_labels[0]
					print 'Moving front...'
				elif Key_input[pygame.K_DOWN]:
					ser.write(50)
					temp_label = output_labels[1]
					print 'Moving back...'
				elif Key_input[pygame.K_LEFT]:
					print 'Moving left...'
					temp_label = output_labels[2]
					ser.write(51)
				elif Key_input[pygame.K_RIGHT]:
					print 'Moving right...'
					temp_label = output_labels[3]
					ser.write(52)

				#combination of commands
				elif Key_input[pygame.K_UP] and Key_input[pygame.K_RIGHT]:
					print 'Moving front and right...'
					ser.write(53)
					temp_label = output_labels[3]
				elif Key_input[pygame.K_UP] and Key_input[pygame.K_LEFT]:
					print 'Moving front and left...'
					ser.write(54)
					temp_label = output_labels[2]
				elif Key_input[pygame.K_DOWN] and Key_input[pygame.K_RIGHT]:
					print 'Moving back and right...'
					ser.write(55)
					temp_label = output_labels[3]
				elif Key_input[pygame.K_DOWN] and Key_input[pygame.K_LEFT]:
					print 'Moving back and left...'
					ser.write(56)
					temp_label = output_labels[2]

			elif event.type == pygame.KEYUP:
				ser.write(48)

			break

		#write the input command to the stack
		print 'Collected corresponding human driver input...\n'
		output_labels = np.vstack((output_labels, temp_label))

finally:
	print 'shape of the final input data: ', input_data.shape
	print 'shape of the final output data: ', output_labels.shape

	#save the entire image data and output data into file
	np.savez('/home/kv/Git/AutoCar/Laptop/Training_data/Train_data.npz', train=input_data, labels=output_labels)
	connection.close()
	server_socket.close()
