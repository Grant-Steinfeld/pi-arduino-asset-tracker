import pprint
import serial
import os 
import pynmea2
import requests
import json

mapquestkey=os.environ.get('MAPQUEST_KEY')
max=10

def annotate(bag):
	print(mapquestkey)
	url = f"http://www.mapquestapi.com/geocoding/v1/reverse?key={mapquestkey}&location={bag['latitude']},{bag['longitude']}&includeRoadMetadata=true&includeNearestIntersection=true"


	print(f"about to call url {url}")
	try:
		r = requests.get(url)
		if(r.status_code == 200):		
			rdict = r.json()
			bag['mapquest'] = rdict
		else:
			print(r.status_code)
	except Exception as mapex:
		print(mapex)

	return bag
		


def parseNMEA(lines):
	print(f"about to parse {len(lines)}")
	latitude = None
	longitude = None
	altitude = None
	altitude_units = None

	for l in lines:
		try:
			msg = pynmea2.parse(l)
			longitude = msg.longitude
			latitude = msg.latitude
			altitude = msg.altitude
			altitude_units = msg.altitude_units
		except pynmea2.nmea.ChecksumError as csex:
			continue

	if(latitude is not None and longitude is not None and altitude is not None):
		return {'latitude':latitude, 'longitude':longitude , 'altitude':altitude, 'altitude_units':altitude_units}

	elif(latitude is not None and longitude is not None):
		return {'latitude':latitude, 'longitude':longitude}
	else:
		raise Exception("bah humbug no data found!")



ser = serial.Serial( port='/dev/ttyACM0', baudrate=9600)

print("connected to: " + ser.portstr)

#this will store some lines
lines = []
counter=0

while True:
	s = str(ser.readline())
	ln = (s[2:][:-5])
	if(ln[0:6]=='$GPGGA'):
		lines.append(ln)
		counter = counter + 1

	if(counter == max):
		break
	

print("about to close serial read")
ser.close()

pp = pprint.PrettyPrinter(indent=4)
ret = parseNMEA(lines)

print(ret)
annotated = annotate(ret)
pp.pprint(annotated)
