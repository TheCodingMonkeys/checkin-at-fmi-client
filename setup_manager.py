import os.path 
import urllib, urllib2, time
from datetime import datetime
import sqlite3 as lite

class Setup_Manager:

    def __init__(self, server_address, reading_device, mac):
        self.server_address = server_address
        self.reading_device = reading_device
        self.mac = mac

        self.io_works = False
        self.db_works = False
        self.server_works = False

    def check_io(self):
        if os.path.exists(self.reading_device):
            self.io_works = True
        else:
            self.io_works = False

    def check_db (self):
        try:
            connection = lite.connect('checkIn.db')
            cursor = connection.cursor()
            cursor.execute('create table if not exists checkIns(url text(63), time datetime)')
            data = cursor.fetchone()
            self.db_works = True
        except lite.Error, e:
            self.db_works = False

    def check_server(self):
        url = self.server_address + 'checkin/status/'
        values = {'mac' : self.mac,}

        try:
            print("Checking the server")
            data = urllib.urlencode(values)          
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                self.server_works = True;
                print(url + " accepted us")
            elif response.getcode() == 401:
                self.server_works = False
                print(url + " did not accept us")
        except Exception, detail:
            self.server_works = False
	    print detail
            print("Error conectiong to the server")
