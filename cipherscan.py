#Usual imports
import subprocess, ujson, xmltodict
from flask import Response
from app import app


@app.route('/cipherscan/<target>')
def cipherscan(target):
    try:
        #We run the nmap script inside our Linux machine.
        print("RUNNING : nmap -sV --script ssl-enum-ciphers -p 443 " + target)
        completed = subprocess.run("nmap -sV -oX tmp.xml --script ssl-enum-ciphers -p 443 " + target, shell=True, stdout=subprocess.PIPE)

        #...Then we print the result for debugging purposes
        print('returncode:', completed.returncode)

        output = open("tmp.xml")
        xml_content = output.read()
        output.close()
        dictxml = xmltodict.parse(xml_content)

        output = ujson.dumps(dictxml, indent=4, sort_keys=True)

    #If the process call goes wrong for some reason, we raise an exception.
    #This allows us to keep the program running.
    except subprocess.CalledProcessError as err :
        print('ERROR:', err)
        output = "ERROR: " + completed.stdout.decode('utf-8')

    #We return an HTTP response anyway, error or not.
    return Response(output, mimetype="application/json")