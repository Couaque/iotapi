#!/bin/bash
echo "Please run this script with yavs' folder as your current folder !"

echo "Installing Python3 and PIP from APT..."
apt install python3 python3-pip nmap python python-pip git gunicorn -y

echo "Installing Python modules from pip3 repos..."
pip3 install flask ujson whatportis xmltodict regex sqlmap

echo "Install Python 2 dependancies"
pip install six

#echo "Installing Python 2 dependencies..."

echo "Installing Mozilla Cipher Scanner..."
git clone https://github.com/mozilla/cipherscan

./cipherscan/cipherscan --curves -j google.com

#git clone https://github.com/offensive-security/exploitdb.git /opt/exploitdb
#sed 's|path_array+=(.*)|path_array+=("/opt/exploitdb")|g' /opt/exploitdb/.searchsploit_rc > ~/.searchsploit_rc
#ln -sf /opt/exploitdb/searchsploit /usr/local/bin/searchsploit