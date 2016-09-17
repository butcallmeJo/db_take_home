#!/usr/bin/env python

'''
Daemon that once every 10 seconds, writes out the average queries per 
second per status code per route and total from a given log called 
access.log.
'''

import daemon
import time
import sys
import os

def get_info(log_path):
    counter = 0 # counting each second
    while True:
        try:
            log = open(log_path, 'r', os.O_NONBLOCK)
            prev_pos = log.seek(0)
            while True:
                # print "before tell"
                where = log.tell()
                # print "after tell / before realine"
                line = log.readline()
                # print "after readline |%s|" % line
                if where == prev_pos:
                    print "break one loop"
                    break
                if not line:
                    time.sleep(0.001) # not good
                    log.seek(where)
                else: 
                    print line,
                    counter += 1
                    prev_pos = where
                    print counter
        except e:
            print e

def run_daemon(log_path):
    '''simple function to run the daemon'''
    with daemon.DaemonContext(stdout=sys.stdout):
        get_info(log_path)


if __name__ == "__main__":
    log_path = "/home/jodag/Dev/personal/db_take_home/access.log" # put the path of the log here
    # run_daemon(log_path)
    get_info(log_path)