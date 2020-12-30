# Dev Install

 TODO - Add notes here for how to open PR, suggest features, etc.

1. Download a copy of missed-moment to your local computer

    ```
        git clone git@github.com:oudeismetis/missed-moment.git
    ```
1. Install the OS on the Pi using method of choice.  e.g. [Raspberry Pi Imager](https://www.raspberrypi.org/documentation/installation/installing-images/) or [NOOBS](https://www.raspberrypi.org/downloads/noobs/) 
1. Boot into the Raspberry Pi
1. Make sure you've enabled the camera module in the settings
1. Install GPAC to do video format operations and exfat-fuse for USB support

    ```
        sudo apt update
        sudo apt install gpac
        sudo apt install exfat-fuse
    ```

1. Install Python libraries

    ```
        pip3 install -r requirements.txt
    ```

1. Copy the `missed-moment` directory to `/home/pi/`

1. Startup the application

    ```
        cd /home/pi/missed-moment
        python3 missed-moment.py
    ```
1. missed-moment is ready for use, push the button to save a moment!
