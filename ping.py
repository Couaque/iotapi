import subprocess, ujson
from flask import Response
from main import app

@app.route('/ping/<target>')
def ping(target):
    try:
        print("RUNNING : ping -c4 " + target)
        completed = subprocess.run("ping -c4 " + target, shell=True, stdout=subprocess.PIPE)

        output = completed.stdout.decode('utf-8')
        print(output)
        print('returncode:', completed.returncode)

        output = output.split("\n")
        
    except subprocess.CalledProcessError as err:
        print('ERROR:', err)
        output = "ERROR: " + err

    return Response(ujson.dumps(output), mimetype="application/json")