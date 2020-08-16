from os import listdir
from os.path import exists, expanduser, isfile
import re
from subprocess import CalledProcessError, check_call
import logging

from pyudev import Context, Monitor

video_pattern = re.compile('missed-moment.*merged.*mp4')
MEDIA_DIR = '/missed_moment_media'
USB_MOUNT_DIR = '/missed_moment_usb'
USB_DIR = USB_MOUNT_DIR + '/missed_moment'


def _copy_files():
    logging.info('==============')
    logging.info('Writing files to attached USB device')
    for filename in listdir(MEDIA_DIR):
        full_path = f'{MEDIA_DIR}/{filename}'
        dest = f'{USB_DIR}/{filename}'
        if video_pattern.fullmatch(filename) and isfile(full_path):
            logging.info(f'Moving {full_path} to {dest}')
            # TODO test via su to the user running the process
            try:
                check_call(['sudo', 'cp', full_path, dest])
            except CalledProcessError as e:
                logging.error(f'Error while copying file {e}')
            # TODO if is_old > delete
    logging.info('Done copying files')


def _process_usb(device):
    device_name = device.device_node  # gets name e.g. /dev/sda1
    # TODO - simple security?
    # if device.get('ID_FS_LABEL', '').lower() == 'missed':
    try:
        # if mount folder exists, always delete folder and create again
        if exists(USB_MOUNT_DIR):
            check_call(['sudo', 'rm', '-rf', expanduser(USB_MOUNT_DIR)])
        check_call(['sudo', 'mkdir', expanduser(USB_MOUNT_DIR)])
        check_call(['sudo', 'mount', device_name, expanduser(USB_MOUNT_DIR)])
        # mk dir on usb if doesn't exist
        if not exists(USB_DIR):
            check_call(['sudo', 'mkdir', expanduser(USB_DIR)])
    except CalledProcessError as e:
        logging.error(f'error: {e}')
    else:
        _copy_files()
    finally:
        check_call(['sudo', 'umount', USB_MOUNT_DIR], timeout=60)
        check_call(['sudo', 'eject', device_name], timeout=60)
        logging.info(f'USB {device_name} ejected')


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('starting missed-moment-usb')
    
    context = Context()
    monitor = Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block', device_type='partition')
    monitor.start()

    for device in iter(monitor.poll, None):
        if device.action == 'add':
            _process_usb(device)
    logging.info('missed-moment-usb ready')


if __name__ == '__main__':
    main()
