import io
import socket
import struct
from PIL import Image

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

try:
	while True:
		image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
		if not image_len:
			break

		image_stream = io.BytesIO()
		image_stream.write(connection.read(image_len))

		image_stream.seek(0)
		image = Image.open(image_stream)
		print 'Image dimensions are: %dx%d', image.size
		image.verify()
		print 'image is verified'

finally:
	connection.close()
	server_socket.close()















