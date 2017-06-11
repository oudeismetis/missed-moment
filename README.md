# missed-moment

A running camera feed that only saves videos when you press a button. How many times has someone done something funny and you said "I wish I got that on camera!" Maybe you did :)

## Project Status

As of 06/11/2017, this project is in the "working prototype" phase of development. It will work, but please be patient with any bugs you are certain to encounter and any holes you may find in this documentation.

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
1. SD card with NOOBS (minimum 4GB)
1. Network access to the Pi (wifi for Pi3, ethernet for Pi2)
1. Suggest wall mountable case for the Pi ([Vilros](http://www.vilros.com/) has a good case with a mount for the camera)

## Installation

1. Install [NOOBS](https://www.raspberrypi.org/downloads/noobs/) on the Pi
1. Boot into the Raspberry Pi
1. Make sure you've enabled the camera module in the settings
1. NOOBS comes preconfigured with two versions of Python with 2.7 being the default. We use 3.5+, so setup [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) in the project directory and switch the python verion
1. If your Raspberry Pi has 3.4 instead, follow [these instructions](http://wyre-it.co.uk/blog/latestpython/) to install.
1. open terminal

    ```
        git clone git@github.com:oudeismetis/missed-moment.git
        cd missed-moment
        virtualenv -p /usr/bin/python3.5 venv
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

- While ssh'd onto the raspberry pi

    ```
        tail -f /var/log/missed-moment.log
    ```

or

    ```
        tail -f /var/log/missed-moment-usb.log
    ```

- If no log appears, check for the presence of `/var/run/missed-moment*.pid`
- A missing file there means the process is not running.
- If there is a file there, the contents will have a process id
- run `top` and look for that process id. You should see that a python process is running.
- Note that the `missed-moment-usb` process is an optional process that only does work when it detects that a USB memory stick has been connected
- The main application is just called `missed-moment`
