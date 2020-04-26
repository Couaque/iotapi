#!/bin/python3
import ujson
import sys
import subprocess
from flask import Flask, Response, request
from app import app

#Filter Information
filter_target = ["+ Target IP:", "+ Target Hostname:", "+ Target Port:"]
filter_ignore = ["+ End Time:", "+ Start Time:"]

#Below is to make the findings filtering more elegant later
#filter_findings = ["+ End Time:", "+ Start Time:", "-----",
# "+ Target IP:", "+ Target Hostname:", "+ Target Port:", "+ Server:"]

#Result Holders
server_version = ""
target_information = []
findings = []
output = []

#Function that draws a line
def draw_line():
    print("*" * 50)

#Function that outputs final results
def results():
    print("HELLO")
    global target_information
    global server_version
    draw_line()
    #print("Web Server Version: " + server_version)
    #draw_line()
    #print("\n")
    for line in target_information:
        placeholder_1 = line.replace("+", '   ')
        print(placeholder_1)
    #print("\n")
    #print("******************* FINDINGS *********************")
    #print("\n")
    for line in findings:
        placeholder_2 = line.replace("+", "[*]")
        print(placeholder_2)


@app.route("/webappscan/<target>")
def webappscan(target):
    findings.clear()
    print("Reached the HTTP listener !")
    command = subprocess.run("nikto -h " + target, shell=True, stdout=subprocess.PIPE)
    global output
    output = command.stdout.decode('utf-8')
    output = output.split("\n")
    #Call the collector function which will filter output
    for line in output:
        if line.startswith("+ Server:"):
            line.replace("+ Server: ", '')
        if line.startswith(tuple(filter_target)):
            target_information.append(line)
        if line.startswith(tuple(filter_ignore)):
            pass
        #The ugly filtering begins, will do this differently later..
        if not "item(s) reported" in line and not "host(s) tested" in line and not "+ End Time:" in line and not "+ Start Time:" in line and not "-----" in line and not "+ Target IP:" in line and not "+ Target Hostname:" in line and not "+ Target Port:" in line and not "+ Server:" in line and not "- Nikto" in line:
            findings.append(line)  
    return Response(ujson.dumps(findings), mimetype="application/json") 
    
