"""
 Semaphore - Mailbox
 Mailbox Device component of Semaphore
 See https://shlchoi.github.io/semaphore/ for more information about Semaphore

 camera_test.py
 Copyright (C) 2017 Samson H. Choi, Matthew Leung

 See https://github.com/shlchoi/semaphore-mailbox/blob/master/LICENSE for license information
 """

from tsl2561 import TSL2561


luminosity_sensor = TSL2561(debug=1)

def read_luminosity():
    print(int(luminosity_sensor.lux()))


def main():
    while(True):
        read_luminosity()


if __name__ == "__main__":
    main()
