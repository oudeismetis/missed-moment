from datetime import datetime
import logging
from os.path import exists, expanduser
from os import popen, kill, system
from signal import SIGTERM, SIGKILL
import subprocess
from subprocess import check_call

from gpiozero import Button
import picamera

# TODO from export.slack import slack

MEDIA_DIR = '/missed_moment_media'
TIME_TO_RECORD = 30  # in seconds
AUDIO_CAPTURE_REMOTE_PORT = 7777

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


def get_capture_device_id():
    device_id = None
    devices = popen("arecord -l")
    device_string = devices.read()
    device_string = device_string.split("\n")
    for line in device_string:
        if(line.find("card") != -1):
            device_id = "hw:" + line[line.find("card")+5] + "," + line[line.find("device")+7]
    return device_id
    

def start_audio_server(device_id):
    print("Starting audio server")
    audio_server_pid = popen("ps -ef | grep [j]ackd | awk '{print $2}'")
    audio_server_pid_string = audio_server_pid.read()
    audio_server_pid_string = audio_server_pid_string.split("\n")
    for line in audio_server_pid_string:
        if line:
            print(f'!!!!!!kill jackd {line}')
            kill(int(line), SIGTERM)
    # TODO document what the parameters mean
    command = f"jackd -P70 -p16 -t2000 -dalsa -d{device_id} -p128 -n3 -r44100 -s &"
    system(command)


def start_audio_capture_ringbuffer():
    print("Starting audio capture buffer")
    audio_capture_pid = popen("ps -ef | grep [j]ack_capture | awk '{print $2}'")
    audio_capture_pid_string = audio_capture_pid.read()
    audio_capture_pid_string = audio_capture_pid_string.split("\n")
    for line in audio_capture_pid_string:
        if line:
            print(f'!!!!!!kill jack_capture {line}')
            kill(int(line), SIGKILL)

    # check UDP port available, TODO make more robust
    remote_port = popen("sudo netstat | grep {}".format(str(AUDIO_CAPTURE_REMOTE_PORT)))
    remote_port_string = remote_port.read()
    if remote_port_string:
        print('Audio capture remote port not available')
    
    # jack_capture called with -O <udp-port-number>can be remote-controlled via OSC (Open Sound Control) messages"
    # jack_capture doesn't like to be spawned as a background process (&)
    # TODO JUDY filename
    filename = "timemachine.wav"
    command = f"jack_capture -O {str(AUDIO_CAPTURE_REMOTE_PORT)} --port '*' --timemachine --timemachine-prebuffer {str(TIME_TO_RECORD)} --filename-prefix missed-moment- {filename}"
    print(command)
    system(command)

    
def main():
    logging.basicConfig(level=logging.INFO)

    # TODO JUDY create service file for jackd?  Or just start jackd when missed-moment starts via python
    # so we can start it with the correct deviceId
    # TODO JUDY start jackd and get the processId so can kill later
    #   command: ps -ef | grep [j]ackd
    #   command:  jackd -P70 -p16 -t2000 -dalsa -dhw:1,0 -p128 -n3 -r44100 -s
    # TODO JUDY what exactly are other params?

    # TODO JUDY audio capture
    #   command: ps -ef | grep [j]ack_capture
    # jack_capture called with -O <udp-port-number>can be remote-controlled via OSC (Open Sound Control) messages"
    # command: jack_capture -O 7777 --port '*' --timemachine --timemachine-prebuffer TIME_TO_RECORD --filename-prefix missed-moment- timemachine.wav
    # TODO JUDY check udp port 7777 is not in use
    #   command: sudo netstat | grep 7777
    #   command: oscsend localhost 7777 /jack_capture/tm/start
    #   command: oscsend localhost 7777 /jack_capture/stop
    # TODO JUDY merge video and audio
    #   command: ffmpeg -i missed-moment-2020-07-28-15-19.mp4 -i test.wav -c:v copy -c:a aac -shortest output.mp4

    if not exists(MEDIA_DIR):
        check_call(['sudo', 'mkdir', expanduser(MEDIA_DIR)])
        # add write permissions for all
        check_call(['sudo', 'chmod', 'a+w', expanduser(MEDIA_DIR)])

    # get the audio capture device_id
    device_id = get_capture_device_id()
    if not device_id:
        print('No audio capture device detected')

    # start audio server
    start_audio_server(device_id)

    # start audio capture buffer
    start_audio_capture_ringbuffer()
    
    


    # video
    # camera.start_recording(stream, format='h264')
    # logging.info('missed-moment ready to save a moment!')

    # button.when_pressed = capture_video
    # try:
    #     while True:
    #         camera.wait_recording(1)
    # finally:
    #     camera.stop_recording()


if __name__ == '__main__':
    main()
