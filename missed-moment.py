from datetime import datetime
import dropbox
import os
import picamera

from time import sleep
from gpiozero import Button
from gpiozero import LED

DROPBOX_API_KEY = ''

"""
TODO
- environment variables
- Github
- run headless
- figure out filetype issues, converting, etc.
- Video playback speed?
- audio?
- Wall mountable case with camera holder
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
    file_name = datetime.now().strftime('%Y-%m-%d-%H-%M.h264')
    stream.copy_to(file_name)
    led.off()
    os.system('MP4Box -add {} {}'.format(file_name, file_name + '.mp4'))
    dbx.files_upload('foo', '/home/pi/' + file_name + '.mp4')

camera.start_recording(stream, format='h264')
camera.start_preview()

try:
    while True:
        camera.wait_recording(1)
        button.when_pressed = capture_video
finally:
    camera.stop_recording()
    # TODO - Stream needs to be stopped???
    camera.stop_preview()

# button.wait_for_press()
# camera.start_recording('/home/pi/video.h264')
# sleep(10)