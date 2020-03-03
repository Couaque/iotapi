# YAVS

Service scanning API, primarily targeted towards IOT devices.
This is written entirely in Python and runs using Flask to serve HTTP requests.

The point of this project is to allow a user to perform automated analysis of an endpoint

## Usage
Please use this project with a compatible client to make it work as intended. You can also use the endpoints provided and call them directly in your browser.

As this program is intended as being as straightforward as possible a simple GET request is enough to get information on a target.

For example, you can use :
```
wget http://<your_ip>/portscan/<target_ip>
```
To get a JSON file listing the ports that are open on your target IP.

If you have any problems, want to make an improvement to the code or want to report a bug, please open a ticket here and I'll take a look to make sure I can fix it for you.

## Installation
### Automated installation
Please use the provided shell script to install this on your Debian or Ubuntu machine.
You can also run this on WSL if you don't already have an Ubuntu machine installed.

Something like this should work :
```
git clone https://github.com/Couaque/yavs
cd yavs
sudo ./install.sh
```
Once it's installed, you will have to run the API on your machine for it to respond to HTTP requests :
```
export FLASK_APP=app.py
flask run
```
### Manual installation
You will still have to clone this Git repository, but you will have to install the different Python dependancies before using this software :
* **pip3** for package management
    * **flask**
    * **ujson**
* **python3** to run the code
