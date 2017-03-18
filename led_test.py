from gpiozero import LED
from time import sleep

led1 = LED(5)
led2 = LED(6)
led3 = LED(13)

led1.on()
led2.on()
led3.on()

sleep(10)

led1.off()
led2.off()
led3.off()
