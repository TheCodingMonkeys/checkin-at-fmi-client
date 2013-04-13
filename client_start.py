import sys
import subprocess
import os.path

import sqlite3 as lite

from uuid import getnode as get_mac
mac = get_mac() # mac adress as 48bit intiger

db_status = True
server_status = True
io_status = True

def check_db ():
	try:
		connection = lite.connect('checkIn.db')
		cursor = connection.cursor()
		cursor.execute('create table if not exists checkIns(url text(63), time datetime)')
		data = cursor.fetchone()
	except lite.Error, e:
		global db_status
		db_status = False

def check_io ():
	if not os.path.exists("/dev/video0"):
		global io_status
		io_status = False
		
def check_server():
		import urllib, urllib2, time

		url = 'http://10.0.200.190:8000/checkin/status/'

		values = {'mac' : mac,}
		global server_status
		try:
			data = urllib.urlencode(values)          
			req = urllib2.Request(url, data)
			response = urllib2.urlopen(req)
			the_page = response.read() 
	 		if the_page == "ok":
				server_status = True;
			else:
				server_status = False
		except Exception, detail:
			server_status = False

def report_error():
	if not db_status:
		print "db_status error!"
	if not server_status:
		print "server_status error!"
	if not io_status:
		print "io_status error!"

def scan():
	from qrtools import QR
	subprocess.call(["sudo", "fswebcam", "-d", "/dev/video0", "scanned.jpg"])
	currentCode = QR(filename=u"scanned.jpg")
	currentCode.decode()
	return currentCode.data
		
check_io()
check_db()
check_server()
report_error()

if io_status & db_status:
	print scan();
	#Everything is ok, so waith for card
	