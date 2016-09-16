# db_take_home
db take home interview assignment

Dropbox SRE Take Home
Gmetric Take-Home: Holberton/Hackbright

Instructions
Background Information

We’ve just turned up a new service. Each time someone accesses this new service, we track information about the request by writing a line to a log file. This file will have the following format:


    $ip_address\t$method $route\t$status_code\t$response_bytes

An example might look like:


    10.0.0.0    GET /    200    2314
    10.0.0.0    POST /   500    324
    10.0.0.0    GET /    404    233
    10.0.0.0    GET /    200    2314

The service will receive many requests per second. To prevent the log file from becoming too large the service will rotate the log at a regular interval. This involves moving the current log to a new location and opening a new file.

In order to understand how this service is doing, we want to gather some stats about what sort of traffic this service is receiving. This information can help us understand how many users are using this service at any given time, how many errors users are seeing, and can eventually help us understand when things aren’t running as expected. In order to do this, we’ll be gathering information about which routes are seeing traffic, what kind of return codes those routes are seeing, and outputting this information in a way that could eventually be consumed by some monitoring system.

There are two ways we could run our code that processes this log file and sends the information off to ganglia, a one off script run through cron or a daemon. While both have their pros and cons, we’re going to implement a daemon that is constantly running and consuming the log file.

We’ll be providing you with a tool that is constantly writing to the log file that you will be parsing.

Task

Using the example log file contents above we want to write a program that runs continuously processing the log file as new lines are written. Every 10 seconds we should print a report that shows the average requests per second received since the last report in the following output:


    $datetime_of_report
    =============================
    $route\t$status\t$qps
    $route\t$status\t$qps
    $route\t$status\t$qps
    

An example might look like:


    Fri Sep  9 11:43:14 2016
    =============================
    /      200    10.3
    /      500    0.1
    /help  200    3.2
    
    Fri Sep  9 11:43:24 2016
    =============================
    /      200    11.3
    /help  200    4.1
    /      500    0.09

Use this code to generate an example log file for testing:

https://www.dropbox.com/s/ghqwaglj4gtsycz/webserver.py?dl=0


https://www.dropbox.com/s/ghqwaglj4gtsycz/webserver.py?dl=0

You can run this code by saving the file locally and running the following:


    python webserver.py --output-file=/home/kelsey/access.log

If you need it, you can add an additional flag to change how frequently the logs rotate:


    python webserver.py --output-file=/home/kelsey/access.log --log-rotation-interval=10


To Do
1. Describe some of the pros and cons to using cron and using a daemon.
2. Make a daemon that once every 10 seconds, writes out the average queries per second per status code per route and total from a given log called access.log.


Extra Tips
- Feel free to use whatever language you feel most comfortable writing in.
- You can use any resources at your disposal to research and come up with a solution to this problem.
- If you get stuck, reach out to us and we’ll be happy to help.
