#This is the main file for the vulnerability scanning API.
#You'll find that this file is very small. It's only job is to initialize the Flask server,
#and to respond to requests coming to the root URL (/)
from flask import Flask, escape, request, Response

#We need this for the Flask server to run
app = Flask(__name__)

#We need this line to import the different Python files for
#each feature. This is vital as well.
import ping, portscan

#Code executed when someone reached out to the / path
@app.route('/')
def main():
    return Response('Root directory of the API !')