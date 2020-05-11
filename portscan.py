import subprocess, ujson, socket, threading, sys, time
from flask import Response
from app import app
from threading import Thread, Lock
from queue import Queue

from concurrent.futures import ThreadPoolExecutor
import threading
import random

#We create the job queue to store all the jobs that we will give to threads.
q = Queue()

#This function will open a socket to a single port.
#This is called by whipper to take a port from the job queue and check it.
def scan_single_port(target, portnb, buffer):

    #We open the TCP socket
    s = socket.socket()
    #This is a simple loading percentage allowing to see if the command is loading fast or not,
    #Without taking a look at the timer at the end
    print(str((portnb / 1024) * 100), end = '\r')

    #We try to connect to the specific port. 
    try:
        s.settimeout(0.1)
        s.connect((target,portnb))
        s.close()
        buffer.append(portnb)
        return True
    except:
        s.close()
        return True
    #If we can connect, we print that the port is open and add it to the list of open ports in buffer
    s.close()
    return True


#This is the function we call when the user reaches
@app.route('/portscan/<target>')
#We have a special route here allowing us to choose what number of workers we want to run our port scanning.
#The optimal one should be "number of cores - 1"
@app.route('/portscan/<target>/<workers>')
@app.route('/portscan/<target>/<workers>/<portlimit>')
def portscan(target, workers = 3, portlimit = 1024):

    #We start the timer to see how much time it took to run the port scan.
    #This is for debugging purposes
    starttime = time.time()
    if portlimit != 1024 :
        portlimit = atoi(portlimit)
    
    
    #We create the array with the list of open ports that we will find in the future
    buffer =[]

    #We create our ThreadPoolExecutor to run the port scan on our pool of ports
    executor = ThreadPoolExecutor(max_workers=workers)
    
    #We scan all ports in the range, created a thread for each of them
    for port in range(1, portlimit) :
        executor.submit(scan_single_port, target, port, buffer)        

    #Now, we wait for a response from each port
    executor.shutdown(wait=True)

    #We create the dictionary that will be converted to JSON for the response
    res=dict()

    #For each port that is open
    for port in buffer:
        #We run whatportis to get the database info about the ports in the shell
        tmp_thr=subprocess.run("whatportis " + str(port) + " --json", shell=True, stdout=subprocess.PIPE)
        #Then decode the output.
        output = tmp_thr.stdout.decode('utf-8')
        #We print it for good measure.
        print(output)
        #If we get infos about the open port, we add it to the port info
        if output[0] == '[' : 
            output = ujson.loads(output)
            res[str(port)] = output
        #If we don't have anything about this port, we just put NO INFO instead.
        else:
            res[str(port)] = "NO INFO"

    #We print the time it took for the code to run
    print('Portscan executed in %s seconds' % (time.time() - starttime))
    #And return the HTTP response with the JSON inside by converting the dictionary in JSON format
    return Response(ujson.dumps(res), mimetype="application/json")