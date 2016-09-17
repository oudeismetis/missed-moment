from datetime import datetime
import os
import subprocess

from decouple import config
from dropbox import Dropbox, files as dbx_files
from gpiozero import Button
import picamera


FILE_CHUNK_SIZE = 100 * 1024 * 1024  # 100MB
DROPBOX_API_KEY = config('DROPBOX_API_KEY', default=None)
button = Button(26)


def upload_dropbox_file_chucks(file_path, file_size):
    dbx = Dropbox(DROPBOX_API_KEY)
    f = open(file_path, 'rb')
    session = dbx.files_upload_session_start(f.read(FILE_CHUNK_SIZE))
    cursor = dbx_files.UploadSessionCursor(
        session_id=session.session_id, offset=f.tell())
    commit = dbx_files.CommitInfo(path=file_path)
    while f.tell() < file_size:
        if ((file_size - f.tell()) <= FILE_CHUNK_SIZE):
            dbx.files_upload_session_finish(
                f.read(FILE_CHUNK_SIZE), cursor, commit)
        else:
            dbx.files_upload_session_append(
                f.read(FILE_CHUNK_SIZE), cursor.session_id, cursor.offset)
            cursor.offset = f.tell()


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

        file_size = os.path.getsize(clean_file)
        if file_size <= FILE_CHUNK_SIZE:
            dbx = Dropbox(DROPBOX_API_KEY)
            f = open(clean_file, 'rb')
            dbx.files_upload(f, clean_file)
        else:
            upload_dropbox_file_chucks(clean_file, file_size)
    except subprocess.CalledProcessError as e:
        print('Error while running MP4Box - {}'.format(e))
    except Exception as e:
        print('Unhandled exception while uploading files - {}'.format(e))


# Main Function
with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    # Keep a buffer of 60sec. (Actually ends up being ~120 for some reason)
    stream = picamera.PiCameraCircularIO(camera, seconds=60)
    camera.start_recording(stream, format='h264')
    button.when_pressed = capture_video
    try:
        while True:
            camera.wait_recording(1)
    finally:
        camera.stop_recording()
