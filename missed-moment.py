from datetime import datetime
import subprocess

from gpiozero import Button
import picamera

button = Button(26)
camera = picamera.PiCamera()
camera.resolution = (1280, 720)
# Keep a buffer of 60sec. (Actually ends up being ~120 for some reason)
stream = picamera.PiCameraCircularIO(camera, seconds=60)


def capture_video():
    file_name = datetime.now().strftime('%Y-%m-%d-%H-%M')

    # Grab 5 more seconds of video
    camera.wait_recording(5)

    # Write current stream to file
    raw_file = '/tmp/' + file_name + '.h264'
    stream.copy_to(raw_file)

    # Convert to .mp4 and upload
    clean_file = '/tmp/' + file_name + '.mp4'
    mp4box_cmd = 'MP4Box -fps 30 -add {} {}'.format(raw_file, clean_file)
    try:
        subprocess.run(mp4box_cmd, shell=True, check=True)

        # TODO - previous dropbox logic started here
    except subprocess.CalledProcessError as e:
        print('Error while running MP4Box - {}'.format(e))
    except Exception as e:
        print('Unhandled exception while uploading files - {}'.format(e))


def main():
    camera.start_recording(stream, format='h264')
    button.when_pressed = capture_video
    try:
        while True:
            camera.wait_recording(1)
    finally:
        camera.stop_recording()

if __name__ == '__main__':
    main()
