"""
 Semaphore - Mailbox
 Mailbox Device component of Semaphore
 See https://shlchoi.github.io/semaphore/ for more information about Semaphore

 camera_test.py
 Copyright (C) 2017 Samson H. Choi, Matthew Leung

 See https://github.com/shlchoi/semaphore-mailbox/blob/master/LICENSE for license information
 """

from gpiozero import LED
from time import sleep

led1 = LED(5)
led2 = LED(6)
led3 = LED(13)

led1.on()
led2.on()
led3.on()

sleep(300)

led1.off()
led2.off()
led3.off()
