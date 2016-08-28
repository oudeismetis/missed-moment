from datetime import datetime
import dropbox
import os
import picamera

# from time import sleep
from decouple import config
from gpiozero import Button
from gpiozero import LED

DROPBOX_API_KEY = config('DROPBOX_API_KEY', default=None)

"""
TODO
- install script for requirements (gpac, dropbox, python-decouple)
- run headless
- figure out filetype issues, converting, etc.
- Video playback speed?
- audio?
- increase quality? Contrast? etc.
"""

button = Button(17)
led = LED(4)
camera = picamera.PiCamera()
# camera.rotation = 180
stream = picamera.PiCameraCircularIO(camera, seconds=60)
dbx = dropbox.Dropbox(DROPBOX_API_KEY)


def capture_video():
    led.on()
    camera.wait_recording(5)
    file_name = datetime.now().strftime('%Y-%m-%d-%H-%M')
    raw_file = '/tmp/' + file_name + '.h264'
    mp4box_file = '/tmp/m_' + file_name + '.mp4'
    avconv_file = '/tmp/a_' + file_name + '.mp4'
    stream.copy_to(raw_file)
    led.off()
    # camera.stop_preview()

    # Experiment with MP4Box encoding
    os.system('MP4Box -add {} {}'.format(raw_file, mp4box_file))
    dbx.files_upload('foo', mp4box_file)

    # Experiment with avconv encoding
    os.system('avconv -i {} -vcondec copy {}'.format(raw_file, avconv_file))
    dbx.files_upload('foo', avconv_file)

camera.start_recording(stream, format='h264')
# camera.start_preview()

try:
    while True:
        camera.wait_recording(1)
        button.when_pressed = capture_video
finally:
    camera.stop_recording()
    # TODO - Stream needs to be stopped???


# button.wait_for_press()
# camera.start_recording('/home/pi/video.h264')
# sleep(10)
