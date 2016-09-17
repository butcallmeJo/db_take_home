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

# Global variable for 10 sec worth of lines
ten_sec_log = []

# Global variable for organizing the list above
ten_sec_data = {}

# Format used for randomly generated log lines.
OUTPUT_FORMAT = "{route}\t{status}\t{qps}"

def get_info(log_path):
    global ten_sec_log
    log = subprocess.Popen(['tail', '-F', log_path], \
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p = select.poll()
    p.register(log.stdout)

    while True:
        if p.poll(1):
            ten_sec_log.append(log.stdout.readline(),)

def print_report():
    global ten_sec_data
    global ten_sec_log
    print time.strftime("%a %b\t%d %H:%M:%S %Y", time.localtime())
    print "============================="
    for key in ten_sec_data:
        key_arr = key.split()
        print OUTPUT_FORMAT.format(
            route = key_arr[0],
            status = key_arr[1],
            qps = (ten_sec_data[key])/10.0
        )
    print "total\t" + str(len(ten_sec_log)) + "\n"

def parse_log():
    global ten_sec_log
    global ten_sec_data
    if not ten_sec_log:
        return
    for line in ten_sec_log:
        line = line.split()
        route = line[2]
        status = line[3]
        key = route + ' ' + status
        if key in ten_sec_data:
            ten_sec_data[key] += 1
        else:
            ten_sec_data[key] = 1
    print_report()   
    # print len(ten_sec_log)

def manage_output():
    global ten_sec_log
    global ten_sec_data
    threading.Timer(10, manage_output).start()
    parse_log()
    ten_sec_log = []
    ten_sec_data = {}   

if __name__ == "__main__":
    log_path = "/home/jodag/Dev/personal/db_take_home/access.log" # put the path of the log here
    manage_output()
    get_info(log_path)