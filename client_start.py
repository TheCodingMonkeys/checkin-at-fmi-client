from time import time, sleep
from datetime import datetime
from evdev import InputDevice, categorize, ecodes
from select import select
from setup_manager import Setup_Manager
from uuid import getnode as get_mac
import urllib, urllib2, time

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
	resources = Setup_Manager(server_adress, RFID_device)

	#Check for IO and DB untill they are available
	while (resources.io_status == False or resources.db_status == False):
		resources.check_io()
		resources.check_db()
		resources.check_server()
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