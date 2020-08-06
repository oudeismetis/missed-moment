#!/bin/bash

APP_HOME=/home/pi/missed-moment
SYSTEMD_HOME=/etc/systemd/system
MM_AUDIO_SERVER_SERVICE=missed-moment-audio-server.service
MM_SERVICE=missed-moment.service
MM_USB_SERVICE=missed-moment-usb.service

echo missed-moment install starting...

cd $APP_HOME
echo installing libraries...
sudo apt update

# video
sudo apt -y install gpac

# USB
sudo apt -y install exfat-fuse

# audio server
sudo apt -y install jackd2
# modify /etc/security/limits.d/audio.conf to bring realtime priorities to the audio group (which is usually fine for a single user desktop usage)
sudo mv /etc/security/limits.d/audio.conf.disabled /etc/security/limits.d/audio.conf
# audio capture
sudo apt -y install liblo-tools
sudo apt -y install jack-capture

pip3 install -r $APP_HOME/requirements.txt

# TODO
# jackd works command line but not as a systemd service file
# added environment variables to service file
# updated /boot/config.txt gpu_mem from 128 -> 256, still have the error of Cannot lock down 13589280 byte memory area (Cannot allocate memory)
# apart of "try", commenting out for now
# echo installing $MM_AUDIO_SERVER_SERVICE...
# sudo cp $APP_HOME/scripts/$MM_AUDIO_SERVER_SERVICE $SYSTEMD_HOME
# sudo chmod 644 $SYSTEMD_HOME/$MM_AUDIO_SERVER_SERVICE
# sudo systemctl start $MM_AUDIO_SERVER_SERVICE
# sudo systemctl enable $MM_AUDIO_SERVER_SERVICE

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
echo Logout and login again for the audio server to have configuration recognized - no need to reboot/restart