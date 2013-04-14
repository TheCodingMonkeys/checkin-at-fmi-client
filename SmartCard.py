#!/usr/bin/python
from uuid import getnode as get_mac
mac = get_mac() # mac adress as 48bit intiger
from datetime import datetime

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
		        return True;
		else:
		        return False
	except Exception, detail:
		return False

check_server()
while True:
	card_code = raw_input('Choose a number')
	import urllib, urllib2, time
	
        url = 'http://10.0.200.190:8000/checkin/'
	
        values = {'mac' : mac,'key' : card_code,'time' : datetime.now()}
        global server_status
        try:
                data = urllib.urlencode(values)
                req = urllib2.Request(url, data)
                response = urllib2.urlopen(req)
                the_page = response.read()
                if the_page == "ok":
                        print "Tuka e"
                else:
                        print "Nqma go"
        except Exception, detail:
                print "Ne se conectna"

