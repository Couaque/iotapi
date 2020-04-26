#Usual imports
import subprocess, ujson
from flask import Response
from app import app

#This code will be executed when the URL is reached.
#<target> means that we give it a parameter
@app.route('/ping/<target>')
def ping(target):
    try:
        #We run the ping command inside our Linux machine.
        print("RUNNING : ping -c4 " + target)
        completed = subprocess.run("ping -c4 " + target, shell=True, stdout=subprocess.PIPE)

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
        output[0] == "ERROR"
        output[1] = completed.stdout.decode('utf-8')

    #We return an HTTP response anyway, error or not.
    return Response(ujson.dumps(output), mimetype="application/json")