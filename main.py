from flask import Flask, escape, request, Response
import ujson, subprocess

from subprocess import check_output

app = Flask(__name__)


@app.route('/ping/<target>')
def ping(target):
    try:
        print("RUNNING : ping -c4 " + target)
        completed = subprocess.run("ping -c4 " + target, shell=True, stdout=subprocess.PIPE)

        output = output = completed.stdout.decode('utf-8')
        print(output)
        print('returncode:', completed.returncode)

        output = output.split("\n")
        
    except subprocess.CalledProcessError as err:
        print('ERROR:', err)
        output = "ERROR: " + err

    return Response(ujson.dumps(output), mimetype="application/json")