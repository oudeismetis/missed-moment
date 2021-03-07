#!/bin/bash

USER=pi
HOME=/home/$USER
APP_HOME=$HOME/missed-moment
SYSTEMD_HOME=/etc/systemd/system
MM_SERVICE=missed-moment.service
MM_USB_SERVICE=missed-moment-usb.service

echo "Starting missed-moment install..."

cd $HOME
echo "Updating OS and installing system dependencies..."
sudo apt update

# video
sudo apt -y install gpac

# USB
sudo apt -y install exfat-fuse

# audio server
sudo apt -y install jackd2
# jackd2 package installation includes /etc/security/limits.d/audio.conf, but just in case run command to
# bring realtime priorities to the audio group (which is usually fine for a single user desktop usage)
sudo dpkg-reconfigure -p high jackd
# audio capture
sudo apt -y install liblo-tools
sudo apt -y install jack-capture

echo "Downloading missed-moment..."
curl -L https://github.com/oudeismetis/missed-moment/archive/master.zip > missed-moment-master.zip
unzip -q missed-moment-master.zip && mv missed-moment-master missed-moment
rm missed-moment-master.zip
cd $APP_HOME

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "Installing $MM_SERVICE..."
sudo cp $APP_HOME/scripts/$MM_SERVICE $SYSTEMD_HOME
sudo chmod 644 $SYSTEMD_HOME/$MM_SERVICE
# use restart so if it started in previous install this will restart, otherwise just starts
sudo systemctl restart $MM_SERVICE
sudo systemctl enable $MM_SERVICE

echo "Installing $MM_USB_SERVICE..."
sudo cp $APP_HOME/scripts/$MM_USB_SERVICE $SYSTEMD_HOME
sudo chmod 644 $SYSTEMD_HOME/$MM_USB_SERVICE
# use restart so if it started in previous install this will restart, otherwise just starts
sudo systemctl restart $MM_USB_SERVICE
sudo systemctl enable $MM_USB_SERVICE

echo "Reloading systemctl units..."
sudo systemctl daemon-reload

# install crontab
chmod a+x $APP_HOME/scripts/missed-moment-delete-files.sh
crontab -u $USER $APP_HOME/scripts/crontab-missed-moment

echo "*************************************"
echo "missed-moment install complete."
echo "*************************************"
echo "*****Reboot to ensure all installed dependencies work as expected.*****"
