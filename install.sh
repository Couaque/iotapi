#!/bin/bash

echo "Installing Python3 and PIP from APT..."
apt install python3 python3-pip nmap -y

echo "Installing Python modules from pip repos..."
pip3 install flask ujson whatportis xmltodict