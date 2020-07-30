#!/bin/bash

APP_HOME=/home/pi/missed-moment
SYSTEMD_HOME=/etc/systemd/system
MM_SERVICE=missed-moment.service
MM_USB_SERVICE=missed-moment-usb.service

echo missed-moment install starting...

cd $APP_HOME
echo installing libraries...
sudo apt update
sudo apt install gpac
sudo apt install exfat-fuse
pip3 install -r $APP_HOME/requirements.txt

echo installing $MM_SERVICE...
sudo cp $APP_HOME/scripts/$MM_SERVICE $SYSTEMD_HOME
sudo chmod 644 $SYSTEMD_HOME/$MM_SERVICE
sudo systemctl start $MM_SERVICE
sudo systemctl enable $MM_SERVICE

echo installing $MM_USB_SERVICE...
sudo cp $APP_HOME/scripts/$MM_USB_SERVICE $SYSTEMD_HOME
sudo chmod 644 $SYSTEMD_HOME/$MM_USB_SERVICE
sudo systemctl start $MM_USB_SERVICE
sudo systemctl enable $MM_USB_SERVICE

sudo systemctl daemon-reload

echo missed-moment install complete.