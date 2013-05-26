from time import time, sleep
from evdev import InputDevice, categorize, ecodes
from select import select
from setup_manager import Setup_Manager

RFID_device = '/dev/input/event0'
server_adress = 'http://87.121.57.184:8000/'
RFID_code_length = 10;

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
			print cartKey[0:RFID_code_length]
			cartKey = ""