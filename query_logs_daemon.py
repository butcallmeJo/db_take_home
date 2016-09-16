#!/usr/bin/env python

'''
Daemon that once every 10 seconds, writes out the average queries per 
second per status code per route and total from a given log called 
access.log.
'''

import daemon
import time
import sys

def get_info(log_path):
    print "test info"
    while True:
        # print "test inf loop"
        with open(log_path, 'r') as log:
            print "test open log"
            print log
            print log.tell()
        time.sleep(10)

def run_daemon(log_path):
    '''simple function to run the daemon'''
    print "test run"
    # out = open('log_averages', 'w+')
    with daemon.DaemonContext(stdout=sys.stdout):
        # func
        sys.stdout.write("test run")
        get_info(log_path)


if __name__ == "__main__":
    print "test main"
    log_path = sys.argv[1]
    run_daemon(log_path)