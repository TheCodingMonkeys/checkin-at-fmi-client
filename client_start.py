from time import time, sleep

from setup_manager import Setup_Manager


if __name__ == '__main__':
	setup_manager = Setup_Manager('http://87.121.57.184:8000/', '/dev/video0')

    while (resources.io_status == Falsem and resources.db_status == False):
	    resources.check_io()
	    resources.check_db()
	    resources.check_server()
	    #sleep(5)
