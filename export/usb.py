from os import listdir
from os.path import exists, expanduser, isfile
import re
from subprocess import CalledProcessError, check_call

from pyudev import Context, Monitor

video_pattern = re.compile('missed-moment.*mp4')
MEDIA_DIR = '/missed_moment_media'
USB_DIR = '/missed_moment_usb'


def _copy_files():
    print('==============')
    print('Writing files to attached USB device')
    for filename in listdir(MEDIA_DIR):
        full_path = '{}/{}'.format(MEDIA_DIR, filename)
        dest = '{}/{}'.format(USB_DIR, filename)
        if video_pattern.fullmatch(filename) and isfile(full_path):
            print('Moving {} to {}'.format(full_path, dest))
            # TODO test via su to the user running the process
            try:
                check_call(['sudo', 'cp', full_path, dest])
            except CalledProcessError as e:
                print('Error while copying file {}'.format(e))
            # TODO if is_old > delete
    print('Done copying files')


def _process_usb(device):
    device_name = device.get('DEVNAME', '/dev/sda1')
    # TODO - simple security?
    # if device.get('ID_FS_LABEL', '').lower() == 'missed':
    try:
        if not exists(USB_DIR):
            check_call(['sudo', 'mkdir', expanduser(USB_DIR)])
            check_call(['sudo', 'mount', device_name, expanduser(USB_DIR)])
    except CalledProcessError as e:
        print('error: {}'.format(e))
    else:
        _copy_files()
        check_call(['sudo', 'udisks', '--unmount', device_name], timeout=60)
    check_call(['sudo', 'udisks', '--eject', '/dev/sda'], timeout=60)
    if exists(USB_DIR):
        check_call(['sudo', 'rm', '-rf', expanduser(USB_DIR)])
    print('USB {} ejected'.format(device_name))


def main():
    context = Context()
    monitor = Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block', device_type='partition')
    monitor.start()

    for device in iter(monitor.poll, None):
        if device.action == 'add':
            _process_usb(device)


if __name__ == '__main__':
    main()
