#Usual imports
import subprocess, ujson
from flask import Response
from app import app


@app.route('/cipherscan/<target>')
def cipherscan(target):
    try:
        #We run the nmap script inside our Linux machine.
        print("RUNNING : nmap -sV --script ssl-enum-ciphers -p 443 " + target)
        completed = subprocess.run("nmap -sV --script ssl-enum-ciphers -p 443 " + target, shell=True, stdout=subprocess.PIPE)

        #We decode the output as UTF-8...
        output = completed.stdout.decode('utf-8')

        #...Then we print the result for debugging purposes
        print(output)
        print('returncode:', completed.returncode)

        #To make this easier I split the single string corresponding with the console result
        #In an array of multiple lines, by spiting the string in a new array cell every time
        #there is a return character, \n
        output = output.split("\n")
        
    #If the process call goes wrong for some reason, we raise an exception.
    #This allows us to keep the program running.
    except subprocess.CalledProcessError as err :
        print('ERROR:', err)
        output = "ERROR: " + completed.stdout.decode('utf-8')

    #We return an HTTP response anyway, error or not.
    return Response(ujson.dumps(output), mimetype="application/json")