# missed-moment

A running camera feed that only saves videos when you press a button. How many times has someone done something funny and you said "I wish I got that on camera!" Maybe you did :)

## Project Status

As of 08/28/2016, this project is in the "working prototype" phase of development. It will work, but please be patient with any bugs you are certain to encounter and any holes you may find in this documentation.

## TODO

1. install script for requirements (gpac, dropbox, python-decouple)
1. run headless instructions
1. figure out filetype issues, converting, etc.
1. Video playback speed?
1. audio?
1. increase quality? Contrast? etc.

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
        pip install python-decouple
        pip install dropbox
        pip install picamera
        pip install gpiozero
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
    ```

## Other Considerations

- You will need a `.env` file in the root of your project that defines the following keys:


    ```
        DROPBOX_API_KEY=[Get a folder-specific APP key connected to your Dropbox account]
    ```
