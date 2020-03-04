#Usual imports
import subprocess, ujson, re, xmltodict
from flask import Response
from app import app


@app.route('/cipherscan/<target>')
def cipherscan(target):
    try:
        #We run the Mozilla binary inside our Linux machine.
        print("RUNNING : ./cipherscan/cipherscan -j --curves " + target)
        completed = subprocess.run("./cipherscan/cipherscan -j --curves " + target, shell=True, stdout=subprocess.PIPE)

        #We decode the output as UTF-8...
        output = completed.stdout.decode('utf-8')

        #...Then we print the result for debugging purposes
        print(output)
        print('returncode:', completed.returncode)

    #If the process call goes wrong for some reason, we raise an exception.
    #This allows us to keep the program running.
    except subprocess.CalledProcessError as err :
        print('ERROR:', err)
        output = "ERROR: " + completed.stdout.decode('utf-8')

    #We return an HTTP response anyway, error or not.
    return Response(output, mimetype="application/json")
