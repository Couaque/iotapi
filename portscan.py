import subprocess, ujson, socket, threading, sys, time
from flask import Response
from main import app
from threading import Thread, Lock
from queue import Queue

q = Queue()

def scan_single_port(target, portnb, buffer):
    s = socket.socket()
    try:
        s.settimeout(0.1)
        s.connect((target,portnb))
    except:
        return True
    else:
        print("Port " + str(portnb) + " open")
        buffer.append(portnb)
        return False
    return None

def whipper(target, port, buffer):
    global q
    port = q.get()
    scan_single_port(target, port, buffer)
    q.task_done()
    print("Number of threads : " + str(threading.active_count()))
        

@app.route('/portscan/<target>')
def portscan(target):
    starttime= time.time()
    buffer=[]
    for port in range(1,65535) :
        q.put(port)
        t = Thread(target=whipper, args=(target,port,buffer,))
        t.setDaemon(True)
        t.start()

    q.join()
    res=dict()
    for port in buffer:
        print(port)
        tmp_thr=subprocess.run("whatportis " + str(port) + " --json", shell=True, stdout=subprocess.PIPE)
        output = tmp_thr.stdout.decode('utf-8')
        print(output)
        if output[0] == '[' : 
            output = ujson.loads(output)
            res[str(port)] = output
        else:
            res[str(port)] = "NO INFO"

    print('Portscan executed in %s seconds' % (time.time() - starttime))
    return Response(ujson.dumps(res), mimetype="application/json")