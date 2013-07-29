from time import time, sleep
from datetime import datetime
from evdev import InputDevice, categorize, ecodes
from select import select
from setup_manager import Setup_Manager
from uuid import getnode as get_mac
import urllib, urllib2, time
import sys, getopt

RFID_device = '/dev/input/event16'
server_adress = 'http://webdream.bg:8000/'
RFID_code_length = 10
mac = get_mac()

def send_code(card_code):
	url = server_adress + 'checkin/'
	now = datetime.now()

	values = {'mac' : mac,'key' : card_code,'time' : now}
	global server_status
	try:
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		the_page = response.read()

		if the_page == "ok":
			print card_code + " checked successfully at " + str(now)
		else:
			print card_code + " check failed at " + str(now)
	except Exception, detail:
		print detail
		print values

if __name__ == '__main__':
	
	if len(sys.argv) <= 1:
		print "Use -start for starting the client in normal mode"
		print "Use -debug for using the debug mode"
		sys.exit(0)

	if sys.argv[1] == "-start":
		resources = Setup_Manager(server_adress, RFID_device, mac)

		#Check for IO and DB untill they are available
		while (resources.io_status == False or resources.db_status == False):
			resources.check_io()
			resources.check_db()
			resources.check_server()
			#TODO: Indicate in some way that we are not ready to work. 
			sleep(3)

		#Start reading from RFID reader
		dev = InputDevice(RFID_device)
		print (dev)

		cartKey = ""
		for event in dev.read_loop():
			if event.type == ecodes.EV_KEY and event.value == 1:
				cartKey += (ecodes.KEY[event.code][-1:])
			if len(cartKey) >= RFID_code_length + 1:
				#We have a code lets send it to the server
				send_code(cartKey[0:RFID_code_length])
				cartKey = ""

	if sys.argv[1] == "-debug":
		resources = Setup_Manager(server_adress, RFID_device, mac)
		resources.check_server()
		if resources.server_status == False:
			print "Not autenticated"
		while 1:
			print "\nPress 1 for 0000000001\nPress 2 for 0000000002\nPress 3 for 0000000003\nOr type a command like [send 1234567890 246473185428129L]"
			command = raw_input();
			if command == "1":
				send_code("0000000001")
			elif command == "2":
				send_code("0000000002")
			elif command == "3":
				send_code("0000000003")