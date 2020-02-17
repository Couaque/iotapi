#Usual imports
import subprocess, ujson
from flask import Response
from app import app

@app.route('/ssl/<target>')
def ssl(target):
    return target