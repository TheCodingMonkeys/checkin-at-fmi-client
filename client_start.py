from time import time, sleep
from datetime import datetime
from evdev import InputDevice, categorize, ecodes
from select import select
from setup_manager import Setup_Manager
import urllib, urllib2, time
import sys, getopt
from threading import Thread
import os.path
import random

def send_alive(resources):
    while True:
        resources.check_server()
        if resources.server_status == False:
            print "Not autenticated"
        sleep(5)

def get_key():
    key_file_name = 'unique.key'

    if os.path.isfile(key_file_name):
        hash_code = tuple(open(key_file_name, 'r'))[0]
    else:
        hash_code = os.urandom(16).encode('hex')
        with open(key_file_name, 'w') as key_file: key_file.write(hash_code)
    
    return hash_code

def send_code(card_code, server_address, device_key):
    url = server_address + 'checkin/'
    time_now = datetime.now()

    values = {'mac' : device_key,'key' : card_code,'time' : time_now}
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
    server_address = 'http://checkin.zala100.com/'
    device_key = get_key()
    resources = Setup_Manager(server_address, reading_device_address, device_key)

    if len(sys.argv) > 1:
        # DEBUG MODE
        while True:
            print "\nPress 0 for sending status code\nPress 1 for 0000000001\nPress 2 for 0000000002\nPress 3 for 0000000003\nOr type a command like [send CODE MAC]"
            command = raw_input();
            if command == "0":
            	resources.check_server()
            elif command == "1":
                send_code("0000000001", server_address, device_key)
            elif command == "2":
                send_code("0000000002", server_address, device_key)
            elif command == "3":
                send_code("0000000003", server_address, device_key)
            else:
                command = command.split()
                code = command[1]
                key = command[2]
                send_code(code, device_key)
    else:
        # NORMAL MODE
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
                    send_code(cart_key[0:10], server_address, device_key)
                    cart_key = ''