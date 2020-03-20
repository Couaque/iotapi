#Imports
import ujson
import requests
import sys
from app import app
from flask import Response, request


#This function takes the full subdomain URL from the subdomains() function, and checks if it's accessible.
def request_subdomain(subdomain_url):
        try:
                # Stores the result of the GET request to the get_response variable
                # If the HTTP response returns with code 200, appends the URL to valid_subdomains list.
                get_response = requests.get(subdomain_url) 
                if str(get_response) ==  "<Response [200]>":
                        print("[+] " + subdomain_url + " is a valid subdomain") 
                        valid_subdomains.append(subdomain_url)
        # If the requests.exceptions.ConnectionError exception is raised, we know the connection failed and move on to the next URL
        except requests.exceptions.ConnectionError:
                pass

#This function iterates through each line of the wordlist and appends this to make a full URL. When the tool finishes running, this function returns the results in JSON.
@app.route('/subdomains/<target>') #URL is now /subdomains?target_url="URL"
def subdomains(target):
        #Might bring back the below 4 lines later...
        # target_url = request.args.get('target_url',default = 1, type = str)
        # target_url = target_url.replace("https://","")
        # target_url = target_url.replace("http://","")
        # target_url = target_url.replace("www.","")
        global valid_subdomains # Make valid_subdomains a global variable
        valid_subdomains = [] # Clear the valid_subdomains list (this is so it doesn't keep appending the previous list if the scan is run more than once)
        # Opens the wordlist file as read-only
        # FOR loop runs through each line of the wordlist file
        wordlist = open("./test_wordlist", "r")
        for each_line in wordlist:
                request_subdomain("http://" + each_line.strip() + "." + target) # Calls the request_subdomain function against each possible subdomain
        else: # When FOR loop finishes:
            return Response(ujson.dumps(valid_subdomains), mimetype="application/json") # Send a response using JSON


