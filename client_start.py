from time import time, sleep
from datetime import datetime
from evdev import InputDevice, categorize, ecodes
from select import select
from setup_manager import Setup_Manager
from uuid import getnode as get_mac
import urllib, urllib2, time
import sys, getopt
from threading import Thread

def send_alive(resources):
    while True:
        resources.check_server()
        if resources.server_status == False:
            print "Not autenticated"
        sleep(5)

def send_code(card_code, server_address, mac_addres):
    url = server_address + 'checkin/'
    time_now = datetime.now()

    values = {'mac' : mac_addres,'key' : card_code,'time' : time_now}
    try:
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)

        if response.getcode() == 200:
            print "checked successfully"
        elif response.getcode() == 401:
            print 'Client is not autenticated'
        elif response.getcode() == 404:
            print 'Server not found'
        print card_code
    except Exception, detail:
        print detail
        print values

if __name__ == '__main__':
    db_name = 'checkIn.db'
    reading_device_address = '/dev/input/event0'
    server_address = 'http://192.168.0.101:8000/'
    mac = get_mac()

    if sys.argv == '-debug':
        # DEBUG MODE
        while True:
            print "\nPress 1 for 0000000001\nPress 2 for 0000000002\nPress 3 for 0000000003\nOr type a command like [send CODE MAC]"
            command = raw_input();
            if command == "1":
                send_code("0000000001", server_address, mac)
            elif command == "2":
                send_code("0000000002", server_address, mac)
            elif command == "3":
                send_code("0000000003", server_address, mac)
            else:
                command = command.split()
                code = command[1]
                mac = command[2]
                send_code(code, mac)
    else:
        # NORMAL MODE
        resources = Setup_Manager(server_address, reading_device_address, mac)

        while not resources.io_works and not resources.db_works:
            resources.check_io()
            resources.check_db()
        
            print 'IO works: ' + str(resources.io_works)
            print 'DB works: ' + str(resources.db_works)
            print '=============='
            sleep(1)
        
        reading_device = InputDevice(reading_device_address)
        print reading_device

        cart_key = ''
        for event in reading_device.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:
                cart_key += (ecodes.KEY[event.code][-1:])

                if ecodes.KEY[event.code][-1:] == 'R': #R is in the end of each code
                    #We have a code lets send it to the server
                    send_code(cart_key[0:10], server_address, mac)
                    cart_key = ''