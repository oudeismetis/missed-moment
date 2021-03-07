from datetime import datetime
import logging
from os.path import exists, expanduser
from os import kill, system
from signal import SIGTERM, SIGKILL
import subprocess
from subprocess import check_call, Popen
from shutil import move
from multiprocessing import Process

from gpiozero import Button
from picamera import PiCamera, PiCameraCircularIO

from config import AUDIO_CAPTURE_REMOTE_PORT, AUDIO_CAPTURE_TEMP_FILENAME, MEDIA_DIR, TIME_TO_RECORD

# TODO from export.slack import slack


def capture_video(camera, stream, file_name):
    # Write current stream to file
    raw_file = f'{MEDIA_DIR}/{file_name}.h264'
    stream.copy_to(raw_file, seconds=TIME_TO_RECORD)  # copy specific number of seconds from stream

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


def capture_audio(file_name):
    # Write current stream to file
    clean_file = f'{MEDIA_DIR}/{file_name}.wav'
    logging.debug(f'audio_clean_file:{clean_file}')

    # get size of the default time machine file, and as soon as it is bigger we know
    # time machine has started recording to file
    result = Popen(f"ls -la {AUDIO_CAPTURE_TEMP_FILENAME} | awk '{{print $5}}'", shell=True, stdout=subprocess.PIPE)
    default_file_size_string = result.stdout.read().decode('utf-8')
    logging.debug(f'initial {AUDIO_CAPTURE_TEMP_FILENAME} size:{default_file_size_string}')

    # timemachine start and jack_capture stop to get the audio ring buff stream saved to file
    # don't think I can use subprocess.call to wait because this is a oscsend command
    command = f"oscsend localhost {AUDIO_CAPTURE_REMOTE_PORT} /jack_capture/tm/start"
    system(command)

    file_saved = False
    while not file_saved:
        result = Popen(f"ls -la {AUDIO_CAPTURE_TEMP_FILENAME} | awk '{{print $5}}'", shell=True, stdout=subprocess.PIPE)
        curr_file_size_string = result.stdout.read().decode('utf-8')
        logging.debug(f'current {AUDIO_CAPTURE_TEMP_FILENAME} size:{curr_file_size_string}')
        if int(curr_file_size_string) > int(default_file_size_string):
            logging.debug(f'{AUDIO_CAPTURE_TEMP_FILENAME} saved')
            file_saved = True

    command = f"oscsend localhost {AUDIO_CAPTURE_REMOTE_PORT} /jack_capture/stop"
    system(command)

    # wait until jack_capture process is stopped
    capture_still_running = True
    while capture_still_running:
        result = Popen(f"ps -ef | grep [j]ack_capture | awk '{{print $2}}'", shell=True, stdout=subprocess.PIPE)
        audio_server_pid_string = result.stdout.read().decode('utf-8')
        logging.debug(f'audio_server_pid_string:{audio_server_pid_string}')
        if not audio_server_pid_string:
            logging.debug('audio capture stopped running')
            capture_still_running = False

    # rename capture file
    logging.debug(f'moving {AUDIO_CAPTURE_TEMP_FILENAME} to {clean_file}')
    move(AUDIO_CAPTURE_TEMP_FILENAME, clean_file)


def merge_video_audio(file_name):
    # Write current stream to file
    clean_file = f'{MEDIA_DIR}/{file_name}-merged.mp4'

    # merge video and audio file, length being shorter of the two
    command = f"ffmpeg -i {MEDIA_DIR}/{file_name}.mp4 -i {MEDIA_DIR}/{file_name}.wav -c:v copy -c:a aac -shortest {clean_file}"
    try:
        subprocess.run(command, shell=True, check=True)
        logging.debug(f'finished creating merged_clean_file:{clean_file}')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error while running merge - {e}')
    except Exception as e:
        logging.error(f'Unhandled exception merge - {e}')


def capture_video_audio(camera, stream):
    file_name = f'missed-moment-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
    # capture video and audio both need to happen in parallel
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
    # resets video stream to empty
    stream.clear()
    logging.info('missed-moment reset and ready to save a moment!')


def get_capture_device_id():
    device_id = None
    result = subprocess.run(['arecord', '-l'], stdout=subprocess.PIPE)
    device_string = result.stdout.decode('utf-8').split("\n")
    for line in device_string:
        if line.find("card") != -1:
            device_id = "hw:" + line[line.find("card")+5] + "," + line[line.find("device")+7]
    logging.debug(f'device_id: {device_id}')
    return device_id


def start_audio_server(device_id):
    # jackd parameters:
    # --no-mlock: doesn't work
    # -p: port max
    # -t: timeout in milliseconds
    # -d: driver backend
    #   -dalsa -C provide only capture ports
    #   -p: period - This value must be a power of 2, and the default is 1024
    #   -n: number of periods of playback latency
    #   -r: sample rate, default is 48000
    #   -s: softmode - this makes jack less likely to disconnect unresponsive ports
    #       when running without --realtime
    logging.info("Starting audio server")
    result = Popen("ps -ef | grep [j]ackd | awk '{print $2}'", shell=True, stdout=subprocess.PIPE)
    audio_server_pid_string = result.stdout.read().decode('utf-8').split('\n')
    logging.debug(f'Audio server pid string[{audio_server_pid_string}]')
    for line in audio_server_pid_string:
        if line:
            logging.debug(f'stopping already running jackd {line}')
            kill(int(line), SIGTERM)
    # NOTE:  Want this to be running as just one background process, e.g.
    # pi@raspberrypi:~/missed-moment $ ps -ef | grep jack
    # pi       10814     1  3 15:19 ?        00:00:04 jackd -P70 -p16 -t2000 -dalsa -dhw:1,0 -p128 -n3 -r44100 -s
    # NOT e.g.
    # pi       11010 10990  0 15:23 ?        00:00:00 /bin/sh -c jackd -P70 -p16 -t2000 -dalsa -dhw:1,0 -p128 -n3 -r44100 -s
    # pi       11011 11010  5 15:23 ?        00:00:00 jackd -P70 -p16 -t2000 -dalsa -dhw:1,0 -p128 -n3 -r44100 -s
    command = f"jackd -P70 -p16 -t2000 -dalsa -d{device_id} -p128 -n3 -r44100 -s &"
    system(command)
    logging.debug(f'jackd start command issued')


def start_audio_capture_ringbuffer():
    logging.info("Starting audio capture buffer")
    result = Popen("ps -ef | grep [j]ack_capture | awk '{print $2}'", shell=True, stdout=subprocess.PIPE)
    audio_capture_pid_string = result.stdout.read().decode('utf-8').split('\n')
    for line in audio_capture_pid_string:
        if line:
            logging.debug(f'stopping already running jack_capture {line}')
            kill(int(line), SIGKILL)

    # check UDP port available, TODO make more robust
    result = Popen(f"sudo netstat | grep {str(AUDIO_CAPTURE_REMOTE_PORT)}", shell=True, stdout=subprocess.PIPE)
    remote_port_string = result.stdout.read().decode('utf-8')
    if remote_port_string:
        logging.error(f'Audio capture remote port not available: {remote_port_string}')

    # jack_capture called with:
    #  -O <udp-port-number>: can be remote-controlled via OSC (Open Sound Control) messages"
    #  --timemachine: run in ringbuffer mode
    #  --timemachine-prebuffer: how much time to keep inr ingbuffer in seconds
    command = f"jack_capture -O {str(AUDIO_CAPTURE_REMOTE_PORT)} --daemon --port '*' --timemachine --timemachine-prebuffer {str(TIME_TO_RECORD)} {AUDIO_CAPTURE_TEMP_FILENAME} &"
    logging.debug(command)
    system(command)


def main():
    # upon exiting the with statement, the camera.close() method is automatically called
    with PiCamera() as camera:
        logging.basicConfig(level=logging.DEBUG)

        logging.debug(f'MEDIA_DIR:{MEDIA_DIR}')
        logging.debug(f'TIME_TO_RECORD:{TIME_TO_RECORD},{type(TIME_TO_RECORD)}')
        logging.debug(f'AUDIO_CAPTURE_REMOTE_PORT:{AUDIO_CAPTURE_REMOTE_PORT},{type(AUDIO_CAPTURE_REMOTE_PORT)}')
        logging.debug(f'AUDIO_CAPTURE_TEMP_FILENAME:{AUDIO_CAPTURE_TEMP_FILENAME}')

        logging.info('starting missed-moment')

        button = Button(26)
        camera.resolution = (1280, 720)
        # Keep a buffer of 30sec. (Actually ends up being ~60 for reasons)
        # https://picamera.readthedocs.io/en/release-1.11/faq.html#why-are-there-more-than-20-seconds-of-video-in-the-circular-buffer
        stream = PiCameraCircularIO(camera, seconds=TIME_TO_RECORD)

        if not exists(MEDIA_DIR):
            check_call(['sudo', 'mkdir', expanduser(MEDIA_DIR)])
            # add write permissions for all
            check_call(['sudo', 'chmod', 'a+w', expanduser(MEDIA_DIR)])

        # video
        camera.start_recording(stream, format='h264')

        # get the audio capture device_id
        device_id = get_capture_device_id()
        if not device_id:
            logging.error('No audio capture device detected')

        # start audio server
        start_audio_server(device_id)

        # start audio capture buffer
        start_audio_capture_ringbuffer()

        logging.info('missed-moment ready to save a moment!')
        # pass a lambda function into 'when_pressed' which contains variables the function can access
        button.when_pressed = lambda: capture_video_audio(camera, stream)
        try:
            while True:
                camera.wait_recording(1)
        finally:
            logging.debug('closing camera and audio server')
            camera.stop_recording()


if __name__ == '__main__':
    # import pdb; pdb.set_trace()
    main()
