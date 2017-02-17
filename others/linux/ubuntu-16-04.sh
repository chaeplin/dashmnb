#!/bin/sh

sudo apt-get update
sudo apt-get -y install libudev-dev libusb-1.0-0-dev libfox-1.6-dev
sudo apt-get -y install autotools-dev autoconf automake libtool
sudo apt-get -y install python3-pip git
sudo pip3 install virtualenv

cd ~/
git clone https://github.com/chaeplin/dashmnb && cd dashmnb
virtualenv -p python3 venv3
. venv3/bin/activate
pip install --upgrade setuptools
pip install -r requirements.txt

sudo cp others/linux/51-* /etc/udev/rules.d/

cp dashlib/config.sample.mainnet.remotesvc.py  dashlib/config.py

python dashlib/config.py


python bin/hw-wallet-for-mn.py


