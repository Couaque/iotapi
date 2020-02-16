import subprocess, ujson, socket, threading, sys, time
from flask import Response
from app import app
from threading import Thread, Lock
from queue import Queue

#We create the job queue to store all the jobs that we will give to threads.
q = Queue()

#This function will open a socket to a single port.
#This is called by whipper to take a port from the job queue and check it.
def scan_single_port(target, portnb, buffer):
    #We open the TCP socket
    s = socket.socket()
    #We try to connect to the specific port. 
    try:
        s.settimeout(0.1)
        s.connect((target,portnb))
    #If we can't connect we simply return True
    except:
        return True
    #If we can connect, we print that the port is open and add it to the list of open ports in buffer
    else:
        print("Port " + str(portnb) + " open")
        buffer.append(portnb)
        return False
    #I added a return here, to return an empty object. I doubt that this is useful
    return None

#This function takes a port from the job queue and sends it to scan_single_port
#This allows us to create threads, mostly limited by the power of your CPU.
def whipper(target, port, buffer):
    global q
    #We get a port from the queue
    port = q.get()
    #we give it to the scan_single_port function
    scan_single_port(target, port, buffer)
    #Once it's done we notify the system that it's done.
    q.task_done()
    #Just a quick print to show the current number of threads.
    print("Number of threads : " + str(threading.active_count()))
        

#This is the function we call when the user reaches
@app.route('/portscan/<target>')
def portscan(target):
    threading.stack_size(64*1024)
    #We start the timer to see how much time it took to run the port scan.
    #This is for debugging purposes
    starttime= time.time()
    buffer=[]
    #We scan all ports in the range, created a thread for each of them
    for port in range(1,65535) :
        q.put(port)
        t = Thread(target=whipper, args=(target,port,buffer,))
        t.setDaemon(True)
        t.start()

    #We wait for all threads to be finished before continuing to process the resulting ports
    q.join()
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