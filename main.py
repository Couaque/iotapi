from flask import Flask, escape, request, Response
import ujson, subprocess

from subprocess import check_output

app = Flask(__name__)

import ping