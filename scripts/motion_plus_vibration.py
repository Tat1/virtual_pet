import RPi.GPIO as GPIO
import time
import requests
import datetime

from envirophat import motion, leds

def LoggingData(elapsed):
    print (elapsed)
    now = time.time()

    r = requests.post("https://mysterious-savannah-98391.herokuapp.com/add_data",
                    json={'time': now,
                            'value': elapsed})

    if r.status_code == requests.codes.ok:
            data = r.json()
            print("Data OK: ", data)
    else:
            print("error fetching, status is ", r.status_code)

#time
timestamp = datetime.datetime.now().isoformat()

#When the angle(x) is in the negative the motion should be undetected
#When the angle(x) is in the positive the motion should be detected
#Vibrations
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
#GPIO.setup(16,GPIO.OUT)

#Accelerometer
print("""This example will detect motion using the accelerometer.
Press Ctrl+C to exit.
""")

#x, y, z = motion.accelerometer()
#print(z)

start_time = 0
last_x = 0

try:
    while True:
        x, y, z = motion.accelerometer()
        print(x)
        time.sleep(1)
        if x > 0 and last_x < 0:
            #first time is the package and second is the seconds time
            start_time = time.time()
            print("Motion Detected")
            leds.on()
            print ("Vibration On")
            GPIO.output(18,GPIO.HIGH)
            #GPIO.output(16,GPIO.HIGH)
        elif x < 0 and last_x > 0:
            elapsed = time.time() - start_time
            print("Motion UnDetected")
            leds.off()
            print ("Vibration Off")
            GPIO.output(18,GPIO.LOW)
            #GPIO.output(16,GPIO.LOW)
            LoggingData(elapsed)
#updates x

        last_x = x

except KeyboardInterrupt:
    pass
