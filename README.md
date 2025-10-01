# missed-moment

A running camera feed that only saves videos when you press a button. How many times has someone done something funny and you said "I wish I got that on camera!" Maybe you did :)

## Project Status

NO UPDATES SINCE DECEMBER 2020

It may work, but there may be bugs. If you have any issues, please [open a GitHub
issue](https://github.com/oudeismetis/missed-moment/issues/new). If there is enough interest in this project I'm willing to continue to support it.

For full project details, see [oudeis.co/projects/missed-moment](https://www.oudeis.co/projects/missed-moment/)

<img src="https://www.oudeis.co/img/2025/missed_moment.gif" />

<div align="center">
    <img src="https://www.oudeis.co/img/2025/missed_moment.gif" width="100%" />
</div>
![Missed Moment Example](https://www.oudeis.co/img/2025/missed_moment.gif)

As of 10/2020 with Raspberry Pi OS, this project is in the "Alpha" phase of development. The current version is stable, but major feature, install, etc changes may happen at any time. Please be patient with any bugs you are certain to encounter and any holes you may find in this documentation.

## Installation

### TL/DR 

```
curl -L https://github.com/oudeismetis/missed-moment/raw/master/install.sh | sh
```

### Prerequisites 

1. [Raspberry Pi](https://www.raspberrypi.org/products/)
1. Raspberry Pi [camera module](https://www.raspberrypi.org/products/camera-module-v2/)
1. SD card (minimum 8GB for OS. We recommend 16GB+ for storing video captures)
1. Newer version of Raspberry Pi OS (Will run on an older OS like Raspbian, but may have issues like Python 3.5+ not installed, camera drivers not pre-installed, etc.)
1. Network access to the Pi (Newer models have WiFi/ethernet on the board)
    * Internet is ONLY needed for initial install
1. Recommend a case that has a camera mount and wall mount ([Vilros](http://www.vilros.com/) has a good case with both)
1. Tactile button that can plug into two pins on the Pi board to get input (By default, missed-moment uses GPIO 26/Pin 37 and the Ground on Pin 39 to attach the button [GPIO Reference](https://www.raspberrypi.org/documentation/usage/gpio/)) 
    - here's an [example of one to buy](https://www.amazon.com/Warmstor-3-Pack-Desktop-Button-Computer/dp/B072FMVZJZ/ref=sr_1_3?dchild=1&keywords=2+pin+pc+desktop+power+cable&qid=1596030325&sr=8-3) (or you can make your own)
1. USB microphone

### From Scratch

1. Install the OS on the Pi using method of choice.  e.g. [Raspberry Pi Imager](https://www.raspberrypi.org/documentation/installation/installing-images/)
1. Boot into the Raspberry Pi
1. `Update Software` when prompted and `Restart`
1. Make sure you've enabled the camera module in the settings
    - Menu > `Preferences` > `Interfaces` > Enable `Camera`
1. Then...
    ```
        curl -L https://github.com/oudeismetis/missed-moment/raw/master/install.sh | sh
    ```
1. Reboot to ensure all installed dependencies work as expected
1. missed-moment is ready for use, push the button to save a moment!
    * Wait a moment after startup, then press the button to have it save off the last ~minute of video and audio
    * Wait a moment after capture, then plug in a USB flash drive, wait for the LEDs to stop flashing, and unplug. Any recordings are now on that USB.

## TODO

1. apt-pinning?
1. configuration file for: file deletion, video/audio time up to X seconds
1. run headless instructions (would need to install pip to a minimum)
1. figure out filetype issues, converting, etc.
1. Video playback speed?
1. Video/audio tuning?
1. increase quality? Contrast? etc.
1. USB with NTFS file system support

## Contributing

Details on getting setup via git and contributing back can be found [Here](contributing.md)

## Other Considerations

- missed-moment is a "Security First" IoT project. As such, internet access is not required for those paranoid about a constant running camera in their home. Videos can be retrieved via SSH/SCP or USB dead drop with simple configuration.
    * Internet is ONLY needed for initial install
- Extra features like Dropbox and Slack are unoffically supported and require a `.env` file in the root of your project that define key(s):


### Dropbox
1. Uncomment out the line in `requirements.txt` that installs the dropbox python SDK.
1. Add the following to the `.env` file

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

- missed-moment should be running with the default "pi" user
- missed-moment-usb currently only supports USB with FAT file system

1.  Installation
    - While ssh'd onto the raspberry pi - logs should print to the screen

1.  Production Installation
    - While ssh'd onto the raspberry pi, to view missed-moment/missed-moment-usb status and logs (if you want to tail the logs add "-f" option right after journalctl and before -u option)

    ```
        sudo systemctl status missed-moment
        sudo systemctl status missed-moment-usb
        journalctl -u missed-moment
        journalctl -u missed-moment-usb
    ```

    - While ssh'd onto the raspberry pi, to view crontab logs

    ```
        tail -f /home/pi/missed-moment-delete-files.log
    ```

    - The main application is called `missed-moment`
    - The USB dead drop application is called `missed-moment-usb`
    - run `ps -ef | grep python` to look for both processes running
    - run `top` and look for python process(es)
    - Note that the `missed-moment-usb` process is an optional process that only does work when it detects that a USB memory stick has been connected
    - Files not downloaded within 7 days are deleted (checks at midnight daily)
