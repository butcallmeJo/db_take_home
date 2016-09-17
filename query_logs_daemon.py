#!/usr/bin/env python

'''
Daemon that once every 10 seconds, writes out the average queries per 
second per status code per route and total from a given log called 
access.log.
'''

import threading
import time
import sys
import os
import subprocess
import select

ten_sec_log = []

def get_info(log_path):
    global ten_sec_log
    log = subprocess.Popen(['tail', '-F', log_path], \
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p = select.poll()
    p.register(log.stdout)

    while True:
        if p.poll(1):
            ten_sec_log.append(log.stdout.readline(),)

def manage_output():
    global ten_sec_log
    threading.Timer(10, manage_output).start()
    print ten_sec_log
    # parse ten_sec_log here
    # flush ten_sec_log here

if __name__ == "__main__":
    log_path = "/home/jodag/Dev/personal/db_take_home/access.log" # put the path of the log here
    manage_output()
    get_info(log_path)