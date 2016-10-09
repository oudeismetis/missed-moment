import os

from decouple import config
from dropbox import Dropbox, files as dbx_files

FILE_CHUNK_SIZE = 100 * 1024 * 1024  # 100MB
DROPBOX_API_KEY = config('DROPBOX_API_KEY', default=None)


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


def upload_to_dropbox(video_file_path):
    """
    Dropbox is an unoffical feature - This code worked at one point,
    but official support was removed for several reasons.
    """
    try:
        file_size = os.path.getsize(video_file_path)
        if file_size <= FILE_CHUNK_SIZE:
            dbx = Dropbox(DROPBOX_API_KEY)
            f = open(video_file_path, 'rb')
            dbx.files_upload(f, video_file_path)
        else:
            upload_dropbox_file_chucks(video_file_path, file_size)
    except Exception as e:
        print('Unhandled exception while uploading files - {}'.format(e))
