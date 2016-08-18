import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np

#declare the host and the port 
host = '0.0.0.0'
port = 2222

#declare the server socket object
server_socket = socket.socket()

#bind
server_socket.bind((host, port))

#listen
print 'I am listening to the incoming connections...'
server_socket.listen(0)

#make a file like object using the single connection
connection = server_socket.accept()[0].makefile('rb')
#print 'connected to the client @: ' + addr[0] + ' : ' + addr[1]
frame = 1

try:
	while True:
		image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
		if not image_len:
			break

		image_stream = io.BytesIO()
		image_stream.write(connection.read(image_len))

		image_stream.seek(0)
		#image = Image.open(image_stream)
		#print 'Image dimensions are: %dx%d', image.size
		#print image.mode, image.format
		#print 'Saving image into ~/Git/AutoCar/data: '
        	#image.show()

		#convert stream data into numpy arrays
		img_array = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
		image = cv2.imdecode(img_array, 0)

		#save the images in the folder
		cv2.imwrite('frame{:>05}.jpg'.format(frame), image)
		frame += 1
		cv2.imshow('image', image)
		
		#wait for 10 milliseconds until the key is triggered		
		cv2.waitKey(10) & 0xFF


finally:
	connection.close()
	server_socket.close()















