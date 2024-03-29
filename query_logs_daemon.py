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
import argparse
import sys

# Global variable for 10 sec worth of lines
TEN_SEC_LOG = []

# Global variable for organizing the list above
TEN_SEC_DATA = {}

# Format used for outputting processed log data.
OUTPUT_FORMAT = "{route}\t{status}\t{qps}" # qps is query per seconds

# lock for threading - to not access TEN_SEC_LOG at the same time
LOCK = threading.Lock()

def get_info(log_path):
    """Get every line from the log."""
    global TEN_SEC_LOG
    log = subprocess.Popen(['tail', '-F', log_path], \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = select.poll()
    p.register(log.stdout)

    while True:
        if p.poll(1):
            with LOCK:
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
    with LOCK:
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

def main(argv):
    """Main part of the program."""
    # Parsing with argparse for the log file
    parser = argparse.ArgumentParser(
        description="Process a log in real time"
    )
    parser.add_argument(
        "--input-file", "-i", dest="log_file", metavar='FILE',
        type=str, required=True,
        help=(
            "the file where requests are logged. Full path preferred"
        )
    )
    args = parser.parse_args(argv[1:])
    log_path = args.log_file
    # start the manage_output function before get_info to launch threading
    # before the program loops infinitely in get_info
    manage_output()
    get_info(log_path)

if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        sys.exit()
