from time import time, sleep
from datetime import datetime
from evdev import InputDevice, categorize, ecodes
from select import select
from setup_manager import Setup_Manager
from uuid import getnode as get_mac
import urllib, urllib2, time
import sys, getopt
from threading import Thread

dbname = 'checkIn.db'
RFID_device = '/dev/input/event16'
server_adress = 'http://localhost:8000/'
RFID_code_length = 10
mac = get_mac()

def send_alive(resources):
    while True:
        resources.check_server()
        if resources.server_status == False:
            print "Not autenticated"
        sleep(5)

def send_code(card_code, device_id):
    print "Sending code: ", card_code, "from host: ", device_id 
    url = server_adress + 'checkin/'
    now = datetime.now()

    values = {'mac' : device_id,'key' : card_code,'time' : now}
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

    resources = Setup_Manager(server_adress, RFID_device, mac)

    if sys.argv[1] == "-start":

        thread = Thread(target = send_alive, args = (resources, ))
        thread.start()
        #Check for IO DB untill they are available
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
        while True:
            print "\nPress 1 for 0000000001\nPress 2 for 0000000002\nPress 3 for 0000000003\nOr type a command like [send CODE MAC]"
            command = raw_input();
            mac = get_mac()
            if command == "1":
                send_code("0000000001", mac)
            elif command == "2":
                send_code("0000000002", mac)
            elif command == "3":
                send_code("0000000003", mac)
            else:
                command = command.split()
                code = command[1]
                mac = command[2]
                send_code(code, mac)
