import serial

ser = serial.Serial( port='/dev/ttyACM0', baudrate=9600)

print("connected to: " + ser.portstr)

#this will store the line
line = []
lines = []
max=10
counter=0

while True:
	s = str(ser.readline())
	ln = (s[2:][:-5])
	if(ln[0:6]=='$GPGGA'):

		lines.append(ln)
		counter = counter + 1

	if(counter == max ):
		break
	
for l in lines:
	print(l)

print("about to close")
ser.close()

