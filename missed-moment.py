from datetime import datetime
import dropbox
import os
import picamera

from decouple import config
from gpiozero import Button
from gpiozero import LED

FILE_CHUNK_SIZE = 10 * 1024 * 1024  # 10MB
DROPBOX_API_KEY = config('DROPBOX_API_KEY', default=None)


button = Button(17)
led = LED(4)
dbx = dropbox.Dropbox(DROPBOX_API_KEY)


def upload_dropbox_file_chucks(file_path, file_size):
    f = open(file_path, 'rb')
    upload_session = dbx.files_upload_session_start(f.read(FILE_CHUNK_SIZE))
    cursor = dropbox.files.UploadSessionCursor(
        session_id=upload_session.session_id, offset=f.tell())
    commit = dropbox.files.CommitInfo(path=file_path)
    while f.tell() < file_size:
        if ((file_size - f.tell()) <= FILE_CHUNK_SIZE):
            dbx.files_upload_session_finish(
                f.read(FILE_CHUNK_SIZE), cursor, commit)
        else:
            dbx.files_upload_session_append(
                f.read(FILE_CHUNK_SIZE), cursor.session_id, cursor.offset)
            cursor.offset = f.tell()


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

    file_size = os.path.getsize(clean_file)
    if file_size <= FILE_CHUNK_SIZE:
        f = open(clean_file, 'rb')
        dbx.files_upload(f, clean_file)
    else:
        upload_dropbox_file_chucks(clean_file, file_size)

    led.off()


# Main Function
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
