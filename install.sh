#!/bin/bash

HOME=/home/pi
APP_HOME=$HOME/missed-moment
SYSTEMD_HOME=/etc/systemd/system
MM_SERVICE=missed-moment.service
MM_USB_SERVICE=missed-moment-usb.service
USER=pi

echo missed-moment install starting...

cd $HOME
echo Updating OS and installing system dependencies...
sudo apt-get update

# video
sudo apt-get -y install gpac

# USB
sudo apt-get -y install exfat-fuse

# audio server
sudo apt-get -y install jackd2
# modify /etc/security/limits.d/audio.conf to bring realtime priorities to the audio group (which is usually fine for a single user desktop usage)
# the audio.conf file already exists now, keep here
sudo mv /etc/security/limits.d/audio.conf.disabled /etc/security/limits.d/audio.conf
# audio capture
sudo apt-get -y install liblo-tools
sudo apt-get -y install jack-capture

echo Downloading missed-moment...
curl -L https://github.com/oudeismetis/missed-moment/archive/master.zip > missed-moment-master.zip
unzip -q missed-moment-master.zip && mv missed-moment-master missed-moment
rm missed-moment-master.zip
cd $APP_HOME

echo Installing Python dependencies...
pip3 install -r requirements.txt

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

# install crontab
chmod a+x $APP_HOME/scripts/missed-moment-delete-files.sh
crontab -u $USER $APP_HOME/scripts/crontab-missed-moment

echo *************************************
echo missed-moment install complete.
echo *************************************
echo *****Reboot to ensure all installed dependencies work as expected*****
