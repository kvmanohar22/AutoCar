import io
import socket
import struct
import time
import picamera

#create a host
host = '10.147.39.211'
port = 2222

#establish the connection
client_socket = socket.socket()
client_socket.connect((host, port))

connection = client_socket.makefile('wb')
try:
	print 'Creating the camera object...'
	camera = picamera.PiCamera()
	camera.resolution = (640, 480)
	print 'starting the preview...'
	camera.start_preview()

	#let the camera start 
	time.sleep(2)

	#start the timer	
	print 'starting the timer...'
	start = time.time()
	
	#create a buffered stream to save the images
	stream = io.BytesIO()

	for foo in camera.capture_continuous(stream, 'jpeg'):
		print 'length of the image: ' + str(stream.tell())
		connection.write(struct.pack('<L', stream.tell()))
		#make sure that the length of the image is sent
		connection.flush()
		stream.seek(0)
		#send the image itself
		connection.write(stream.read())
		
		#exit after 30 seconds of streaming
		if time.time()-start > 30:
			break
		stream.seek(0)
		stream.truncate()
	#just send zero length to terminate the connection
	print 'streaming is terminated!'
	connection.write(struct.pack('<L', 0))
			
finally:
	print 'closing the connections...'
	connection.close()
	client_socket.close()



