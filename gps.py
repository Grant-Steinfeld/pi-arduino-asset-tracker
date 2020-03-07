import serial

def parse(lines):
	print("dms")
	#https://gps-coordinates.org/
	for l in lines:
		la = l.split(',')
		long = la[2]
		longC = la[3]
		lat = la[4]
		latC = la[5]
		latDegrees = int(str(float(long)/100).split('.')[0])
		latMinutes = int(str(float(long)/100).split('.')[1][:2])
		inf = {'latDegrees':latDegrees, 'latMinutes':latMinutes, 'lat':long, 'latCardinal': longC, 'long': lat, 'longCardinal': latC}
		print(inf)

ser = serial.Serial( port='/dev/ttyACM0', baudrate=9600)

print("connected to: " + ser.portstr)

#this will store some lines
lines = []
max=10
counter=0

while True:
	s = str(ser.readline())
	ln = (s[2:][:-5])
	if(ln[0:6]=='$GPGGA'):
		lines.append(ln)
		counter = counter + 1
	else:
		print(ln)

	if(counter == max):
		break
	

print("about to close")
ser.close()
parse(lines)

