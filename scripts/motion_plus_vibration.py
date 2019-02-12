import RPi.GPIO as GPIO
import time
import datetime

from envirophat import motion, leds

#time 
timestamp = datetime.datetime.now().isoformat()

#Vibrations
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

#Accelerometer
print("""This example will detect motion using the accelerometer.
Press Ctrl+C to exit.
""")

#x, y, z = motion.accelerometer()
#print(z)

try:
    while True:
        x, y, z = motion.accelerometer()
        print(x)
        time.sleep(1)
        if x > 0:
            print("Motion Detected")
            leds.on()
            print ("Vibration On")
            GPIO.output(18,GPIO.HIGH)
        else:
            print("Motion UnDetected")
            leds.off()
            print ("Vibration Off")
            GPIO.output(18,GPIO.LOW)

except KeyboardInterrupt:
    pass

