"""
 Semaphore - Mailbox
 Mailbox Device component of Semaphore
 See https://shlchoi.github.io/semaphore/ for more information about Semaphore

 camera_test.py
 Copyright (C) 2017 Samson H. Choi, Matthew Leung

 See https://github.com/shlchoi/semaphore-mailbox/blob/master/LICENSE for license information
 """

from gpiozero import LED, Button
from picamera import PiCamera
from tsl2561 import TSL2561
from requests import post
from time import sleep
from enum import Enum
from os.path import isfile
from json import load
from requests import post


debug = False
camera = PiCamera()
led_5 = LED(5)
led_6 = LED(6)
led_13 = LED(13)
luminosity_sensor = TSL2561(debug=1)
idle_light = LED(17)
calibrate_light = LED(27)
calibrate_button = Button(16, pull_up=True)
url = '0.0.0.0:8080'
mailbox_id = ''
luminosity_button = Button(12)


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


def take_picture(filename, num_pictures=1):
    sleep(3)
    led_5.on()
    led_6.on()
    led_13.on()
    sleep(2)

    for i in range(num_pictures):
        sleep(1)
        if num_pictures == 1:
            camera.capture(filename)
        else:
            camera.capture(filename.format(i))

    led_5.off()
    led_6.off()
    led_13.off()


def read_luminosity():
    return int(luminosity_sensor.lux()) > 2


def read_calibrate():
    return not calibrate_button.is_pressed


def send_snapshot():
    endpoint = 'http://{}/snapshot'.format(url)
    headers = {'enctype': 'multipart/form-data'}
    files = {'snapshot': open('snapshot.jpg')}
    data = {'mailbox': mailbox_id}

    if debug:
        return True
    
    r = post(endpoint, headers=headers, data=data, files=files)
    return r.status_code == 200


def send_calibration():
    endpoint = 'http://{}/calibrate'.format(url)
    headers = {'enctype': 'multipart/form-data'}
    files = {'calibrate_0': open('calibrate_0.jpg'), 'calibrate_1': open('calibrate_1.jpg')}
    data = {'mailbox': mailbox_id}

    if debug:
        return True
    
    r = post(endpoint, headers=headers, data=data, files=files)
    return r.status_code == 200


def main():
    print("Copyright (C) 2017 Samson H. Choi, Matthew Leung")
    print("This program comes with ABSOLUTELY NO WARRANTY")
    print("This is free software, and you are welcome to redistribute it under certain conditions")

    load_config('config')
    camera.brightness = 60
    camera.resolution = (640, 480)
    camera.color_effects = (128, 128)

    idle_light.on()    
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
                idle_light.blink(0.5, 0.5)
        elif state == State.CLOSED:
            # mailbox has been closed, do stuff here
            take_picture('snapshot.jpg')
            result = send_snapshot()
            if result:
                idle_light.on()
                calibrate_light.off()
            else:
                idle_light.off()
                calibrate_light.on()
            print("State: IDLE")
            state = State.IDLE
        elif state == State.CALIBRATE_IDLE:
            calibrate_light.on()
            idle_light.on()
            if luminosity:
               print("State: CALIBRATE_OPEN")
               state = State.CALIBRATE_OPEN
        elif state == State.CALIBRATE_OPEN:
            calibrate_light.on()
            idle_light.on()
            if not luminosity:
               print("State: CALIBRATE_CLOSED")
               state = State.CALIBRATE_CLOSED
               calibrate_light.blink(0.5, 0.5)
               idle_light.blink(0.5, 0.5)
        elif state == State.CALIBRATE_CLOSED:
            take_picture('calibrate_{}.jpg', 2)
            result = send_calibration()
            if result:
               calibrate_light.off()
               idle_light.on()
            else:
               calibrate_light.on()
               idle_light.off()
            print("State: IDLE")
            state = State.IDLE


if __name__ == "__main__":
    main()

