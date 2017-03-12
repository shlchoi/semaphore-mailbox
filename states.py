from gpiozero import LED, Button
from requests import post
from time import sleep
from enum import Enum


led_5 = LED(5)
led_6 = LED(6)
led_13 = LED(13)
camera = LED(26)
luminosity_button = Button(12)
calibrate_button = Button(16)


class State(Enum):
    IDLE = 0
    OPEN = 1
    CLOSED = 2
    CALIBRATE_IDLE = 3
    CALIBRATE_OPEN = 4
    CALIBRATE_CLOSED = 5


def take_picture():
    led_5.on()
    led_6.on()
    led_13.on()
    camera.on()
    sleep(5)
    camera.off()
    led_5.off()
    led_6.off()
    led_13.off()


def read_luminosity():
    return luminosity_button.is_pressed


def read_calibrate():
    return calibrate_button.is_pressed


def main():
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
            take_picture()
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
            take_picture()
            print("State: IDLE")
            state = State.IDLE


if __name__ == "__main__":
    main()

