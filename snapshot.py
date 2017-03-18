from gpiozero import LED, Button
from picamera import PiCamera
from requests import post
from time import sleep
from os.path import isfile
from json import load
from requests import post


camera = PiCamera()
led_5 = LED(5)
led_6 = LED(6)
led_13 = LED(13)
url = ''
mailbox_id = ''


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
    sleep(3)
    led_5.on()
    led_6.on()
    led_13.on()
    sleep(3)
    camera.capture(filename)
    led_5.off()
    led_6.off()
    led_13.off()


def send_snapshot():
    endpoint = 'http://{}/snapshot'.format(url)
    headers = {'enctype': 'multipart/form-data'}
    files = {'snapshot': open('snapshot.jpg')}
    data = {'mailbox': mailbox_id}

    r = post(endpoint, headers=headers, data=data, files=files)


def main():
    load_config('config')
    camera.brightness = 60
    camera.resolution = (640, 480)
    camera.color_effects = (128, 128)

    take_picture('snapshot.jpg')
    result = send_snapshot()


if __name__ == "__main__":
    main()


