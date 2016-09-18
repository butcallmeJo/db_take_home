#!/usr/bin/env python

'''
Daemon that once every 10 seconds, writes out the average queries per
second per status code per route and total from a given log called
access.log.
'''

import threading
import time
import subprocess
import select

# Defining what log file to look at
LOG_PATH = "/home/jodag/Dev/personal/db_take_home/access.log" # TODO

# Global variable for 10 sec worth of lines
TEN_SEC_LOG = []

# Global variable for organizing the list above
TEN_SEC_DATA = {}

# Format used for outputting processed log data.
OUTPUT_FORMAT = "{route}\t{status}\t{qps}" # qps is query per seconds

# lock for threading
lock = threading.Lock()

def get_info():
    """Get every line from the log."""
    global TEN_SEC_LOG
    log = subprocess.Popen(['tail', '-F', LOG_PATH], \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = select.poll()
    p.register(log.stdout)

    while True:
        if p.poll(1):
            with lock:
                TEN_SEC_LOG.append(log.stdout.readline(),)

def print_report(nb_lines):
    """Print the report after formatting the data."""
    print time.strftime("%a %b\t%d %H:%M:%S %Y", time.localtime())
    print "============================="
    for key in TEN_SEC_DATA:
        key_arr = key.split()
        print OUTPUT_FORMAT.format(
            route=key_arr[0],
            status=key_arr[1],
            qps=float((TEN_SEC_DATA[key]))/10
        )
    print "total\t%d\n" % (nb_lines)

def parse_log():
    """Parse the log"""
    global TEN_SEC_LOG
    global TEN_SEC_DATA
    # usually used for when log doesn't contain any lines.
    if not TEN_SEC_LOG:
        return
    # copying TEN_SEC_LOG and clearing it so get_info can use it again.
    with lock:
        ten_sec_log_copy = TEN_SEC_LOG
        TEN_SEC_LOG = []
    # looping over the copy to get the correct info and save it in a
    # dictionary for future analysis.
    for line in ten_sec_log_copy:
        line = line.split()
        route = line[2]
        status = line[3]
        key = route + ' ' + status
        if key in TEN_SEC_DATA:
            TEN_SEC_DATA[key] += 1
        else:
            TEN_SEC_DATA[key] = 1
    nb_lines = len(ten_sec_log_copy)
    print_report(nb_lines)

def manage_output():
    """Manage the process for the output."""
    # global TEN_SEC_LOG
    global TEN_SEC_DATA
    threading.Timer(10, manage_output).start()
    parse_log()
    TEN_SEC_DATA = {}

if __name__ == "__main__":
    """Main part of the program."""
    # start the manage_output function which will loop every 10 seconds
    manage_output()
    # start the get_info function that reads the log in constant time
    get_info()
