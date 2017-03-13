from gpiozero import LED, Button
from picamera import PiCamera
from tsl2561 import TSL2561
from requests import post
from time import sleep
from enum import Enum
from os.path import isfile
from json import load
from requests import post


camera = PiCamera()
led_5 = LED(5)
led_6 = LED(6)
led_13 = LED(13)
luminosity_sensor = TSL2561(debug=1)
luminosity_button = Button(12)
calibrate_button = Button(16)
url = ''
mailbox_id = ''


class State(Enum):
    IDLE = 0
    OPEN = 1
    CLOSED = 2
    CALIBRATE_IDLE = 3
    CALIBRATE_OPEN = 4
    CALIBRATE_CLOSED = 5


def load_config(config_path):
    if isfile(config_path):
        config = load(open(config_path, 'r'))
        server_url = config['server_url']
        server_port = config['server_port']
	global url
        url = '{0}:{1}'.format(server_url, server_port)
	global mailbox_id
        mailbox_id = config['mailbox_id']


def take_picture(filename):
    led_5.on()
    led_6.on()
    led_13.on()
    sleep(3)
    camera.capture(filename)
    led_5.off()
    led_6.off()
    led_13.off()


def read_luminosity():
    return int(luminosity_sensor.lux()) > 5


def read_calibrate():
    return calibrate_button.is_pressed


def send_snapshot():
    endpoint = 'http://{}/snapshot'.format(url)
    headers = {'enctype': 'multipart/form-data'}
    files = {'snapshot': open('snapshot.jpg')}
    data = {'mailbox': mailbox_id}

    # r = post(endpoint, headers=headers, data=data, files=files)


def send_calibration():
    endpoint = 'http://{}/calibrate'.format(url)
    headers = {'enctype': 'multipart/form-data'}
    files = {'snapshot': open('calibrate.jpg')}
    data = {'mailbox': mailbox_id}

    # r = post(endpoint, headers=headers, data=data, files=files)


def main():
    load_config('config')
    camera.brightness = 60
    camera.resolution = (640, 480)
    camera.color_effects = (128, 128)

    print(url)
    
    state = State.IDLE
    while True:
        calibrate = read_calibrate()
        luminosity = read_luminosity()

        if state == State.IDLE:
            # default state, waiting for action
            if calibrate:
                print("State: CALIBRATE_IDLE")
                state = State.CALIBRATE_IDLE
            elif luminosity:
                print("State: OPEN")
                state = State.OPEN
        elif state == State.OPEN:
            if calibrate:
                print("State: CALIBRATE_OPEN")
                state = State.CALIBRATE_OPEN
            elif not luminosity:
                print("State: CLOSED")
                state = State.CLOSED
        elif state == State.CLOSED:
            # mailbox has been closed, do stuff here
            take_picture('snapshot.jpg')
            send_snapshot()
            print("State: IDLE")
            state = State.IDLE
        elif state == State.CALIBRATE_IDLE:
            if luminosity:
               print("State: CALIBRATE_OPEN")
               state = State.CALIBRATE_OPEN
        elif state == State.CALIBRATE_OPEN:
            if not luminosity:
               print("State: CALIBRATE_CLOSED")
               state = State.CALIBRATE_CLOSED
        elif state == State.CALIBRATE_CLOSED:
            take_picture('calibrate.jpg')
            send_calibration()
            print("State: IDLE")
            state = State.IDLE


if __name__ == "__main__":
    main()

