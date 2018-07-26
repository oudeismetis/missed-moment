# missed-moment

A running camera feed that only saves videos when you press a button. How many times has someone done something funny and you said "I wish I got that on camera!" Maybe you did :)

## Project Status

As of 07/07/2017, this project is in the "working prototype" phase of development. It will work, but please be patient with any bugs you are certain to encounter and any holes you may find in this documentation.

## TODO

1. run headless instructions
1. figure out filetype issues, converting, etc.
1. Video playback speed?
1. audio?
1. increase quality? Contrast? etc.

## Requirements

1. [Raspberry Pi](https://www.raspberrypi.org/products/)
1. Raspberry Pi [camera module](https://www.raspberrypi.org/products/camera-module-v2/)
1. SD card (minimum 4GB) - Raspbian lite installed (or NOOBS if your are new to the Pi)
1. Suggest wall mountable case for the Pi
Pi 2 or 3 - ([Vilros](http://www.vilros.com/) has a good case with a mount for the camera)
Pi Zero W - ([Pigeon](https://www.thingiverse.com/thing:2230707/#files) Open Source project - Currently testing myself.)
[Adafruit](https://www.adafruit.com/product/3414) also has a decently priced Pi Zero W bundle which includes a case, camera, and camera cable. You'll just need to figure out how/where to mount it.

## Production Install (TODO - Work in progress. Resin? Image?)

### Some initial advice
1. The below steps assume you have a new-ish Raspberry Pi with Raspbian Lite installed. Obviously I don't have time to test older Pis and other setups, but if you run into any problems, please let me know and I'll be happy to document them for others.
1. If you want you are using the Pi Zero W for missed-moment (recommended) and want it wifi connected (optional), I recommend you first get Raspbian working with Wifi enabled on a Pi3, and then just move the micro-SD card over to the Pi Zero. Can be a LOT easier than buying a bunch of micro USB and micro HDMI adapters for the Pi Zero so you can hook up a keyboard and try to configure the wifi.

1. Install raspbian
1. boot the pi and login with default creds - pi/raspberry
1. `sudo raspi-config` - Change password, turn on camera and ssh, and configure keyboard for US
1. Configure [wifi](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)
1. `sudo ifdown wlan0`
1. `sudo ifup wlan0`
1. `sudo ping -c 5 www.google.com`
1. `ifconfig wlan0 | grep "inet addr"` for IP address. Also, IP should display automatically when
   the Pi boots. A few lines above the login prompt it should say "My IP address is..."

### On with the actual install
1. Download the latest release of missed-moment
    ```
        cd /home/pi/
        curl https://codeload.github.com/oudeismetis/missed-moment/zip/master > missed-moment.zip
        unzip missed-moment.zip && mv missed-moment-master missed-moment
        cd missed-moment
    ```
1. Make sure you have pip and virtualenv installed

    ```
        pip3 --version
        sudo apt-get -y install python3-pip



        curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
        sudo python get-pip.py
        sudo pip install virtualenv
        virtualenv -p /usr/local/bin/python3.6 venv
    ```
1. Then get everything running...

    ```
        sudo pip3 install -r requirements.txt
        sudo cp missed-moment.sh /etc/init.d/missed-moment
        sudo chmod +x /etc/init.d/missed-moment
        sudo update-rc.d missed-moment defaults
        sudo service missed-moment start
        sudo cp missed-moment-usb.sh /etc/init.d/missed-moment-usb
        sudo chmod +x /etc/init.d/missed-moment-usb
        sudo update-rc.d missed-moment-usb defaults
        sudo service missed-moment-usb start
    ```

## Development Installation

1. Install [NOOBS](https://www.raspberrypi.org/downloads/noobs/) on the Pi
1. Boot into the Raspberry Pi
1. Make sure you've enabled the camera module in the settings
1. NOOBS comes preconfigured with two versions of Python with 2.7 being the default. We NEED 3.6+, so setup [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) in the project directory and switch the python verion
1. If your Pi has a version older than 3.6 (or no python3 at all), follow [these instructions](https://liftcodeplay.com/2017/06/30/how-to-install-python-3-6-on-raspbian-linux-for-raspberry-pi/) to install.

    ```
        cd /home/pi/
        which git
    ```

if git is not installed (likely)

    ```
        sudo apt-get install git-all
    ```

then...

    ```
        git clone git@github.com:oudeismetis/missed-moment.git
        cd missed-moment
        virtualenv -p /usr/bin/python3.6 venv
    ```


1. Create a .env file at the root of the project. (See below for .env contents)
1. Install GPAC to do video format opperations:

    ```
        sudo apt-get update
        sudo apt-get install gpac
    ```

1. Install Requirements

    ```
        pip install -r requirements.txt
    ```
1. Startup the application:

    ```
        python missed-moment.py
    ```

## Other Considerations

- missed-moment is a "Security First" IoT project. As such, internet access is not required for those paranoid about a constant running camera in their home. Videos can be retrieved via SSH/SCP or USB deaddrop with simple configuration.
- Extra features like Dropbox and Slack are unoffically supported and require a `.env` file in the root of your project that define key(s):


### Dropbox
1. Uncomment out the line in `requirements.txt` that installs the dropbox python SDK.
1. Add the following to you `.env`

    ```
        DROPBOX_API_KEY=[Get a folder-specific APP key connected to your Dropbox account]
    ```

### Slack
1. If you want slack notifications, log into Slack and [create a bot user](https://api.slack.com/bot-users)
1. Uncomment out the line in `requirements.txt` that installs the slack python SDK.
1. Add the following to you `.env`

    ```
        SLACK_API_TOKEN=[Provided when you create a bot user on Slack]
    ```

## USB Camera and/or audio support
Current it is recommended to stick with the Raspberry Pi camera when running missed-moment. Reasons for this:
1. I spent a good amount of time investigating audio support. Will likely revisit in the future,
   but the LOE was a little high. Long story short, keeping video and audio in sync in two seperate
   ring buffers is not easy/obvious.
1. The Raspberry Pi Zero is great for keeping missed-moment cheap, especially since I run multiple
   of them in my house. It also means they can be small and hidden away. Given that the Zero only
   has one USB port available, it makes it a challenge to have a microphone plugged in and/or a USB
   camera and/or have deaddrop support for downloading recorded files. 
For the above two reasons, I have been focusing on a "no audio; no USB" appraoch to missed moment.

## Troubleshooting

- While ssh'd onto the raspberry pi you can watch the log of the two main processes

    ```
        tail -f /var/log/missed-moment.log
        tail -f /var/log/missed-moment-usb.log
    ```

- If no log appears, check for the presence of `/var/run/missed-moment*.pid`
- A missing file there means the process is not running.
- If there is a file there, the contents will have a process id
- run `top` and look for that process id. You should see that a python process is running.
- Note that the `missed-moment-usb` process is an optional process that only does work when it detects that a USB memory stick has been connected
- The main application is just called `missed-moment`
