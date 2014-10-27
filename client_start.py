#!/usr/bin/python
from time import time, sleep
from datetime import datetime
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
    print "sending code"
    print card_code
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
    dev_server_address = 'http://127.0.0.1:8000/'
    # dev_server_address = server_address # DEBUG
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
                send_code("0000000001", dev_server_address, device_key)
            elif command == "2":
                send_code("0000000002", dev_server_address, device_key)
            elif command == "3":
                send_code("0000000003", dev_server_address, device_key)
            else:
                command = command.split()
                code = command[1]
                key = command[2]
                send_code(code, device_key)
    else:
        import serial
        with serial.Serial(port='COM3', baudrate=9600, timeout=1,
                       xonxoff=False, rtscts=False, dsrdtr=True) as s:
            for line in s:
                send_code(line, server_address, device_key)

