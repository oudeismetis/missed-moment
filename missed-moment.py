from datetime import datetime
import logging
from os.path import exists, expanduser
import subprocess
from subprocess import check_call

from gpiozero import Button
import picamera

# TODO from export.slack import slack

MEDIA_DIR = '/missed_moment_media'
TIME_TO_RECORD = 30  # in seconds

button = Button(26)
camera = picamera.PiCamera()
camera.resolution = (1280, 720)
# Keep a buffer of 30sec. (Actually ends up being ~60 for reasons)
# https://picamera.readthedocs.io/en/release-1.11/faq.html#why-are-there-more-than-20-seconds-of-video-in-the-circular-buffer
stream = picamera.PiCameraCircularIO(camera, seconds=TIME_TO_RECORD)


def capture_video():
    file_name = f'missed-moment-{datetime.now().strftime("%Y-%m-%d-%H-%M")}'

    # Grab 5 more seconds of video
    camera.wait_recording(5)

    # Write current stream to file
    raw_file = f'{MEDIA_DIR}/{file_name}.h264'
    stream.copy_to(raw_file, seconds=TIME_TO_RECORD) # copy specific number of seconds from stream

    # Convert to .mp4
    clean_file = f'{MEDIA_DIR}/{file_name}.mp4'
    mp4box_cmd = f'MP4Box -fps 30 -add {raw_file} {clean_file}'
    try:
        subprocess.run(mp4box_cmd, shell=True, check=True)
        # TODO slack(clean_file, file_name)
        # upload_to_dropbox(clean_file)
    except subprocess.CalledProcessError as e:
        logging.error(f'Error while running MP4Box - {e}')
    except Exception as e:
        logging.error(f'Unhandled exception uploading files - {e}')


def main():
    logging.basicConfig(level=logging.INFO)

    # TODO JUDY create service file for jackd?  Or just start jackd when missed-moment starts via python
    # so we can start it with the correct deviceId
    # TODO JUDY get microphone deviceId
    # TODO JUDY start jackd and get the processId so can kill later
    # command:  jackd -P70 -p16 -t2000 -dalsa -dhw:2,0 -p128 -n3 -r44100 -s
    # TODO JUDY what exactly are other params?
    # TODO JUDY audio capture
    # command: jack_capture --port "*" --timemachine --timemachine-prebuffer TIME_TO_RECORD --filename-prefix missed-moment- timemachine.wav
    # TODO JUDY timemachine only works when you hit return to save buffer to disk, but then I would need to immediately escape out

    if not exists(MEDIA_DIR):
        check_call(['sudo', 'mkdir', expanduser(MEDIA_DIR)])
        # add write permissions for all
        check_call(['sudo', 'chmod', 'a+w', expanduser(MEDIA_DIR)])
    camera.start_recording(stream, format='h264')
    logging.info('missed-moment ready to save a moment!')

    button.when_pressed = capture_video
    try:
        while True:
            camera.wait_recording(1)
    finally:
        camera.stop_recording()


if __name__ == '__main__':
    main()
