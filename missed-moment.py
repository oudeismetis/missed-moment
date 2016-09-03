from datetime import datetime
import dropbox
import os
import picamera

from decouple import config
from gpiozero import Button
from gpiozero import LED

DROPBOX_API_KEY = config('DROPBOX_API_KEY', default=None)


button = Button(17)
led = LED(4)
dbx = dropbox.Dropbox(DROPBOX_API_KEY)


def capture_video():
    led.on()
    file_name = datetime.now().strftime('%Y-%m-%d-%H-%M')

    # Grab 5 more seconds of video
    camera.wait_recording(5)

    # Write current stream to file
    raw_file = '/tmp/' + file_name + '.h264'
    stream.copy_to(raw_file)

    # Convert to .mp4 and upload
    clean_file = '/tmp/' + file_name + '.mp4'
    os.system('MP4Box -fps 30 -add {} {}'.format(raw_file, clean_file))
    dbx.files_upload('foo', clean_file)

    led.off()


with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    stream = picamera.PiCameraCircularIO(camera, seconds=60)
    camera.start_recording(stream, format='h264')
    button.when_pressed = capture_video
    try:
        while True:
            camera.wait_recording(1)
    finally:
        camera.stop_recording()
