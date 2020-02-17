#Usual imports
import subprocess, ujson, re
from flask import Response
from app import app


@app.route('/servicescan/<target>/<ports>')
def servicescan(target, ports):
    try:
        #We run the nmap script inside our Linux machine.
        #The -sV 9 option runs all the tests possible for a certain service so we get the best precision
        #We also give it a list of ports so that we don't need to scan everything
        print("RUNNING : nmap -sV 9 -p  " + ports + " " + target)
        completed = subprocess.run("nmap -sV 9 -p " + ports + " " + target, shell=True, stdout=subprocess.PIPE)

        #We decode the output as UTF-8...
        output = completed.stdout.decode('utf-8')

        #...Then we print the result for debugging purposes
        print(output)
        print('returncode:', completed.returncode)

        #To make this easier I split the single string corresponding with the console result
        #In an array of multiple lines, by spiting the string in a new array cell every time
        #there is a return character, \n
        output = output.split("\n")

        #We create a temporary array
        tmp = []
        #We need to compile a regex string to match it against every line of the result
        p = re.compile("[0-9].*/tcp")
        #We go through each line of output
        for line in output:
            #If the regex matches the line...
            if type(p.match(line)) == re.Match :
                #...We add it to tmp
                tmp.append(line)
        #We replace output with the value of tmp to trim all useless lines
        output = tmp
            
        
    #If the process call goes wrong for some reason, we raise an exception.
    #This allows us to keep the program running.
    except subprocess.CalledProcessError as err :
        print('ERROR:', err)
        output = "ERROR: " + completed.stdout.decode('utf-8')

    #We return an HTTP response anyway, error or not.
    return Response(ujson.dumps(output), mimetype="application/json")