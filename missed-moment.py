from datetime import datetime
import subprocess
from os.path import exists, expanduser
from subprocess import check_call

from gpiozero import Button
import picamera

button = Button(26)
camera = picamera.PiCamera()
camera.resolution = (1280, 720)
# Keep a buffer of 60sec. (Actually ends up being ~120 for some reason)
stream = picamera.PiCameraCircularIO(camera, seconds=60)

MEDIA_DIR = '/missed_moment_media'


def capture_video():
    file_name = 'missed-moment-' + datetime.now().strftime('%Y-%m-%d-%H-%M')

    # Grab 5 more seconds of video
    camera.wait_recording(5)

    # Write current stream to file
    raw_file = '{}/{}.h264'.format(MEDIA_DIR, file_name)
    stream.copy_to(raw_file)

    # Convert to .mp4
    clean_file = '{}/{}.mp4'.format(MEDIA_DIR, file_name)
    mp4box_cmd = 'MP4Box -fps 30 -add {} {}'.format(raw_file, clean_file)
    try:
        subprocess.run(mp4box_cmd, shell=True, check=True)

        # TODO - previous dropbox logic started here
    except subprocess.CalledProcessError as e:
        print('Error while running MP4Box - {}'.format(e))
    except Exception as e:
        print('Unhandled exception while uploading files - {}'.format(e))


def main():
    if not exists(MEDIA_DIR):
        check_call(['sudo', 'mkdir', expanduser(MEDIA_DIR)])
    camera.start_recording(stream, format='h264')
    button.when_pressed = capture_video
    try:
        while True:
            camera.wait_recording(1)
    finally:
        camera.stop_recording()

if __name__ == '__main__':
    main()
