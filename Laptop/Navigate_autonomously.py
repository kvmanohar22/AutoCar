import numpy as np
import serial
import socket


params = np.load('/home/kv/Git/AutoCar/parameters.npz')
theta1 = params['theta1']
theta2 = params['theta2']
theta1 = np.matrix(theta1)
theta2 = np.matrix(theta2)
#print 'shape of theta1: ', theta1.shape
#print 'shape of theta2: ', theta2.shape

#functions
def sigmoid(z):
	#print 'In sigmoid...shape : ', z.shape
	#print z[0, 0:5]
	#print (1 / (1 + np.exp(-z[0, 0:5])))
	return (1 / (1 + np.exp(-z)))

def forward_propagate(X, theta1, theta2):
	m = X.shape[0]
	#print 'X shape: ', X.shape
	#print 'theta1 shape: ', theta1.shape
	a1 = np.insert(X, 0, values=np.ones(m), axis=1)
	#print 'a1 layer shape: ', a1.shape
	z2 = a1 * theta1.T 
	#print 'z2 shape: a1 * theta1.T: ', z2.shape
	a2 = np.insert(sigmoid(z2), 0, values=np.ones(m), axis=1)
	#print 'a2 layer shape: ', a2.shape
	#print 'theta2 shape: ', theta2.shape
	z3 = a2 * theta2.T
	#print 'z3 shape: a2 * theta2.T', z3.shape
	h = sigmoid(z3)
	return a1, z2, a2, z3, h

#start the serial port
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

#connect to pi
host = '0.0.0.0'
port = 2222

server_socket = socket.socket()
server_socket.bind((host, port))
print 'I am listening to the incoming connections...'
server_socket.listen(0)
connection = server_socket.accept()[0].makefile('rb')

#start collecting the images
try:
	while True:
		image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
		if not image_len:
			break

		image_stream = io.BytesIO()
		image_stream.write(connection.read(image_len))

		image_stream.seek(0)
		img_array = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
		image2 = cv2.imdecode(img_array, 0)
		
		#rotate the image by 180
		rows, cols = image2.shape
		M = cv2.getRotationMatrix2D((cols/2, rows/2), 180, 1)
		image = cv2.warpAffine(image2, M, (cols, rows))#240x320	

		#select mid half of the image
		temp_image_mat = image[120:240, :]
		temp_image_arr = temp_image_mat.reshape((1, 38400))

		#display the image
		cv2.imshow('input image', image)
		cv2.waitKey(1) & 0xFF

		#predict the steering command
		X = temp_image_arr
		a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2) 
		y = np.array(np.argmax(h, axis=1) + 1) 

		if y == 1:
			print 'forward'
			ser.write(chr(49))
		elif y == 2:
			print 'back'
			ser.write(chr(50))
		elif y == 3:
			print 'left'
			ser.write(chr(51))
		elif y == 4:
			print 'right'
			ser.write(chr(52))
		else:
			print 'invalid!!'

finally:
	connection.close()
	server_socket.close()