from gpiozero import LED
from time import sleep
import picamera
from requests import post
from tsl2561 import TSL2561

led1 = LED(5)
led2 = LED(6)
led3 = LED(13)
camera = picamera.PiCamera()
camera.brightness = 60
camera.resolution = (640, 480)
camera.color_effects = (128, 128)
tsl = TSL2561(debug=1)
var = 1
luxnumber = 0
luxopened = 0

while var == 1:
    luxnumber = int(tsl.lux())
    print(luxnumber)
    if luxnumber > 5:
        var = 0
        sleep(30)
        luxopened = int(tsl.lux())
        print(luxopened)
        if luxopened < 5:
            led1.on()
            led2.on()
            led3.on()
            sleep(3)
            camera.capture('image1.jpg')
            sleep(3)
            led1.off()
            led2.off()
            led3.off()
            url = "http://ec2-54-175-148-98.compute-1.amazonaws.com:5000/snapshot"
            headers = {'enctype': "multipart/form-data"}
            files = {'snapshot': open("/home/pi/image1.jpg")}
            data = {'mailbox': "temp_fd5c7ba5-c2db-4923-8075-046cbead8173"}
    
            r = post(url, headers=headers, data=data, files=files)

            if r.status_code == 200:
                print("Success")
            else:
                print("Failure")

            var = 1




