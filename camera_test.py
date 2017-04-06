"""
 Semaphore - Mailbox
 Mailbox Device component of Semaphore
 See https://shlchoi.github.io/semaphore/ for more information about Semaphore

 camera_test.py
 Copyright (C) 2017 Matthew Leung, Samson H. Choi

 See https://github.com/shlchoi/semaphore-mailbox/blob/master/LICENSE for license information
 """

from gpiozero import LED
from time import sleep
import picamera

image_name = 'empty_{}.jpg'
num_pictures = 1
led1 = LED(5)
led2 = LED(6)
led3 = LED(13)
camera = picamera.PiCamera()
camera.brightness = 60
camera.resolution = (640, 480)
camera.color_effects = (128, 128)

led1.on()
led2.on()
led3.on()

sleep(5)
for i in range(num_pictures):
    camera.capture(image_name.format(i))

sleep(3)
led1.off()
led2.off()
led3.off()
