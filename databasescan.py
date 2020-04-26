#!/usr/bin/env python

import re
import subprocess, ujson
from flask import Response
from app import app

@app.route('/databasescan/<target>')
def databasescan(target):
    res=[]
    target = target.replace("*", "/")
    target = target.replace("@", "?")
    print(target)
    res.append(target)
    try:

        #Run SQLMap on imported website to display available databases
        runsqlmap = subprocess.run("sqlmap -u" + target + " --dbs -batch --threads=4", shell=True, stdout=subprocess.PIPE)
        #converting output to UTF8 for formatting
        output = runsqlmap.stdout.decode('utf-8')
        #splitting each line of output onto a new line
        output = output.split("\n")

        #for loop to display the number of databases and names
        #searches code for "available databases" and prints

        iterate = 0
        lines_to_print = ""
        search_a = "MySQL"

        for line in output:
            if line.startswith("available databases"):
                res.append("[+] The number of " + line)
                res.append("[+] Database names:")
                lines_to_print = re.search(r'\d+', line)
                iterate = int(lines_to_print.group())

            elif (iterate > 0):
                res.append(line)
                iterate = iterate-1

        #run sqlmap to show the underlying databse format used
        runsqlmap2 = subprocess.run("sqlmap -u " + target + " --hostname -batch --threads=4", shell=True, stdout=subprocess.PIPE)
        output2 = runsqlmap2.stdout.decode('utf-8')


        #variable to count how may times "MySQL" appears in string, to be used in searchsploit
        countmysql = output2.count("MySQL")

        version_number=""
        output2 = output2.split("\n")
        for line2 in output2:
            if line2.startswith("back-end DBMS:"):
                res.append("[+] The " + line2)
                lines_to_print = re.search(r'\d+', line2)
                version_number = line2.split(" ")[-1][0:3]

        if countmysql > 0:
            search_a = "MySQL"
        else:
            search_a = 0

        runsqlmap3 = subprocess.run("sqlmap -u " + target + " -b -batch --threads=4", shell=True, stdout=subprocess.PIPE)
        output3 = runsqlmap3.stdout.decode('utf-8')
        output3 = output3.split("\n")
        print(search_a)
        for line3 in output3:
            if line3.startswith("back-end DBMS operating system:"):
                res.append("[+] The " + line3)
                lines_to_print = re.search(r'\d+', line3)

        #print("searchsploit -t " + search_a + " " + lines_to_print)
        print(" search_a is " + str(search_a))
        res.append("YOUR " + str(search_a) + " DATABASE CONTAINS THE FOLLOWING VULNERABILITIES")
        print("searchsploit -t " + str(search_a) + " " + version_number + " --colour")
        runsearchsploit = subprocess.run("searchsploit -t " + str(search_a) + " " + version_number + " --colour", shell=True, stdout=subprocess.PIPE)
        output2 = runsearchsploit.stdout.decode('utf-8')
        output2 = output2.split("\n")
        for line in output2:
            res.append(line)

        print(output2)

    except subprocess.CalledProcessError as err :
        print('ERROR:', err)
        output[0] == "ERROR"
        output[1] = completed.stdout.decode('utf-8')

    return Response(ujson.dumps(res), mimetype="application/json")



