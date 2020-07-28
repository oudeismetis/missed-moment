# missed-moment

A running camera feed that only saves videos when you press a button. How many times has someone done something funny and you said "I wish I got that on camera!" Maybe you did :)

## Project Status

As of 07/28/2020 with "Raspbian GNU/Linux 10 (buster)" OS, this project is in the "working prototype" phase of development. It will work, but please be patient with any bugs you are certain to encounter and any holes you may find in this documentation.

## TODO

1. run headless instructions
1. figure out filetype issues, converting, etc.
1. Video playback speed?
1. audio?
1. increase quality? Contrast? etc.
1. USB export/eject fails? Device specific issue?

## Requirements

1. [Raspberry Pi](https://www.raspberrypi.org/products/)
1. Raspberry Pi [camera module](https://www.raspberrypi.org/products/camera-module-v2/)
1. SD card with Raspbian GNU/Linux 10 OS (minimum OS and SD Card size 4GB)
1. Network access to the Pi (WiFi for Pi3, WiFi/ethernet for Pi2)
1. Suggest wall mountable case for the Pi ([Vilros](http://www.vilros.com/) has a good case with a mount for the camera)
1. Tactile button and female-to-female jumper lead to get input (By default, missed-moment uses GPIO 26/Pin 37 and the Ground on Pin 39 to attach the button [GPI Reference](https://www.raspberrypi.org/documentation/usage/gpio/)) 

## Installation

1. Download a copy of missed-moment to your local computer

    ```
        git clone git@github.com:oudeismetis/missed-moment.git
    ```
1. Install the OS on the Pi using method of choice.  e.g. [Raspberry Pi Imager](https://www.raspberrypi.org/documentation/installation/installing-images/) or [NOOBS](https://www.raspberrypi.org/downloads/noobs/) 
1. Boot into the Raspberry Pi
1. Make sure you've enabled the camera module in the settings
1. Missed moment requires Python 3.5+ to interface with the camera.  Raspbian GNU/Linux 10 OS comes with both Python 2.7 and Python 3.7.
1. Install GPAC to do video format opperations:

    ```
        sudo apt update
        sudo apt install gpac
    ```

1. Install Python libraries

    ```
        pip3 install -r requirements.txt
    ```

1. Copy the `missed-moment` directory to `/home/pi/`

1. Startup the application:

    ```
        cd /home/pi/missed-moment
        python3 missed-moment.py
    ```
1. Missed moment is ready for use, push the button to save a moment!


## Production Install (TODO - Work in progress)

1. Copy the `missed-moment` directory to `/home/pi/`
1. Then...

    ```
        sudo pip3 install -r requirements.txt
        cp missed-moment.sh /etc/init.d/missed-moment
        sudo chmod +x /etc/init.d/missed-moment
        sudo update-rc.d missed-moment defaults
        sudo service missed-moment start
        cp missed-moment-usb.sh /etc/init.d/missed-moment-usb
        sudo chmod +x /etc/init.d/missed-moment-usb
        sudo update-rc.d missed-moment-usb defaults
        sudo service missed-moment-usb start
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
        SLACK_API_TOKEN=[Not supported yet. Work in progress. PR's welcome.]
    ```

## Troubleshooting

1.  Installation
- While ssh'd onto the raspberry pi - logs should print to the screen

1.  Production Installation

- While ssh'd onto the raspberry pi

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
