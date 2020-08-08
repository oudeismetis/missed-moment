from datetime import datetime
import logging
from os.path import exists, expanduser
from os import kill, system, popen
from signal import SIGTERM, SIGKILL
import subprocess
from subprocess import check_call
from shutil import move
from multiprocessing import Process

from gpiozero import Button
import picamera

# TODO from export.slack import slack

MEDIA_DIR = '/missed_moment_media'
TIME_TO_RECORD = 15  # in seconds
AUDIO_CAPTURE_REMOTE_PORT = 7777
AUDIO_CAPTURE_TEMP_FILENAME = f'{MEDIA_DIR}/missed-moment-timemachine.wav'


def capture_video(camera, stream, file_name):
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
        print(f'Error while running MP4Box - {e}')
    except Exception as e:
        print(f'Unhandled exception uploading files - {e}')


def capture_audio(file_name):
    # Write current stream to file
    clean_file = f'{MEDIA_DIR}/{file_name}.wav'
    print(f'audio_clean_file:{clean_file}')

    # timemachine start and jack_capture stop to get the audio ring buff stream
    # don't think I can use subprocess.call to wait because this is a oscsend command
    command = f"oscsend localhost {AUDIO_CAPTURE_REMOTE_PORT} /jack_capture/tm/start"
    system(command)
    # get size of the default time machine file, and as soon as it is bigger we know 
    # time machine has started recording to file
    default_file_size = popen(f"ls -la {AUDIO_CAPTURE_TEMP_FILENAME} | awk '{{print $5}}'")
    default_file_size_string = default_file_size.read()
    print(f'initial {AUDIO_CAPTURE_TEMP_FILENAME} size:{default_file_size_string}')
    file_saved = False
    while not file_saved:
        curr_file_size = popen(f"ls -la {AUDIO_CAPTURE_TEMP_FILENAME} | awk '{{print $5}}'")
        curr_file_size_string = curr_file_size.read()
        print(f'curr {AUDIO_CAPTURE_TEMP_FILENAME} size:{curr_file_size_string}')
        if (int(curr_file_size_string) > int(default_file_size_string)):
            print('file saved!!!')
            file_saved = True

    command = f"oscsend localhost {AUDIO_CAPTURE_REMOTE_PORT} /jack_capture/stop"
    system(command)
    
    # wait until jack_capture process is stopped
    capture_still_running = True
    while capture_still_running:
        audio_server_pid = popen("ps -ef | grep [j]ack_capture | awk '{print $2}'")
        audio_server_pid_string = audio_server_pid.read()
        print(f'audio_server_pid_string:{audio_server_pid_string}')
        if audio_server_pid_string == "":
            print('capture stopped running')
            capture_still_running = False

    # rename capture file
    print(f'moving {AUDIO_CAPTURE_TEMP_FILENAME} to {clean_file}')
    move(AUDIO_CAPTURE_TEMP_FILENAME, clean_file)


def merge_video_audio(file_name):
    # Write current stream to file
    clean_file = f'{MEDIA_DIR}/{file_name}-merged.mp4'
    print(f'merged_clean_file:{clean_file}')

    # merge video and audio file, length being shorter of the two
    command = f"ffmpeg -i {MEDIA_DIR}/{file_name}.mp4 -i {MEDIA_DIR}/{file_name}.wav -c:v copy -c:a aac -shortest {clean_file}"
    # TODO JUDY system(command)

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error while running merge - {e}')
    except Exception as e:
        print(f'Unhandled exception merge - {e}')


def capture_video_audio(camera, stream):
    file_name = f'missed-moment-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
    # both of these to happen in parallel
    p1 = Process(target=capture_video, args=(camera, stream, file_name,))
    p1.start()
    p2 = Process(target=capture_audio, args=(file_name,))
    p2.start()
    p1.join()
    p2.join()

    # merge video and audio
    merge_video_audio(file_name)

    # restart audio capture for next moment
    start_audio_capture_ringbuffer()


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
    command = f"jack_capture -O {str(AUDIO_CAPTURE_REMOTE_PORT)} --daemon --port '*' --timemachine --timemachine-prebuffer {str(TIME_TO_RECORD)} {AUDIO_CAPTURE_TEMP_FILENAME} &"
    print(command)
    system(command)

    
def main():
    # upon exiting the with statement, the camera.close() method is automatically called
    with picamera.PiCamera() as camera:
        print('start')
        #logging.basicConfig(level=logging.INFO)

        # TODO JUDY create service file for jackd?  Or just start jackd when missed-moment starts via python
        # so we can start it with the correct deviceId
        # TODO JUDY start jackd and get the processId so can kill later
        #   command: ps -ef | grep [j]ackd
        #   command:  jackd -P70 -p16 -t2000 -dalsa -dhw:1,0 -p128 -n3 -r44100 -s
        # TODO JUDY what exactly are other params?

        # TODO JUDY audio capture
        #   command: ps -ef | grep [j]ack_capture
        # jack_capture called with -O <udp-port-number>can be remote-controlled via OSC (Open Sound Control) messages"
        # command: jack_capture -O 7777 --port '*' --daemon --timemachine --timemachine-prebuffer TIME_TO_RECORD timemachine.wav &
        # try --hide-buffer-usage and 
        # try --daemon and --absolutely-silent
        # TODO JUDY check udp port 7777 is not in use
        #   command: sudo netstat | grep 7777
        #   command: oscsend localhost 7777 /jack_capture/tm/start
        #   command: oscsend localhost 7777 /jack_capture/stop
        # TODO JUDY merge video and audio
        #   command: ffmpeg -i missed-moment-2020-07-28-15-19.mp4 -i test.wav -c:v copy -c:a aac -shortest output.mp4


        button = Button(26)
        camera.resolution = (1280, 720)
        # Keep a buffer of 30sec. (Actually ends up being ~60 for reasons)
        # https://picamera.readthedocs.io/en/release-1.11/faq.html#why-are-there-more-than-20-seconds-of-video-in-the-circular-buffer
        stream = picamera.PiCameraCircularIO(camera, seconds=TIME_TO_RECORD)

        if not exists(MEDIA_DIR):
            check_call(['sudo', 'mkdir', expanduser(MEDIA_DIR)])
            # add write permissions for all
            check_call(['sudo', 'chmod', 'a+w', expanduser(MEDIA_DIR)])
    
        # video
        print('start video')
        camera.start_recording(stream, format='h264')

        # get the audio capture device_id
        device_id = get_capture_device_id()
        if not device_id:
            print('No audio capture device detected')
        print(device_id)

        # start audio server
        start_audio_server(device_id)  

        # start audio capture buffer
        start_audio_capture_ringbuffer()

        print('missed-moment ready to save a moment!')
        # pass a lambda function into 'when_pressed' which contains variables the function can access
        button.when_pressed = lambda : capture_video_audio(camera, stream)
        try:
            while True:
                camera.wait_recording(1)
        finally:
            print('closing camera and audio server')
            camera.stop_recording()


if __name__ == '__main__':
    main()
