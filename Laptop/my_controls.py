#this is the revised code to get the key pressed by the user
import serial
import time

#start the serial connection
print 'Starting the serial connection...'
print 'Starting in another 3 seconds...'
time.sleep(3)
ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)


while True:
	command = raw_input('Enter (w or s or a or d): ')

	#print 'Entered command: ', command
	#print '\n'

	#send the corresponding serial command to the serial port
	if command == 'w':
		print 'Moving front...'
		ser.write(chr(49))
	elif command == 's':
		print 'Moving back...'
		ser.write(chr(50))
	elif command == 'a':
		print 'Moving left...'
		ser.write(chr(51))
	elif command == 'd':
		print 'Moving right...'
		ser.write(chr(52)) 
	else:
		print 'Invalid character!'



