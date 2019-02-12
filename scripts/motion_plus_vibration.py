import RPi.GPIO as GPIO
import time
import requests
import datetime

from envirophat import motion, leds

def LoggingData():
	now = time.time()

	r = requests.post("https://mysterious-savannah-98391.herokuapp.com/add_data",
                  	json={'time': now,
                        	'value': 1.0})

	if r.status_code == requests.codes.ok:
    		data = r.json()
    		print("Data OK: ", data)
	else:
    		print("error fetching, status is ", r.status_code)

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
	    LoggingData()
        else:
            print("Motion UnDetected")
            leds.off()
            print ("Vibration Off")
            GPIO.output(18,GPIO.LOW)

except KeyboardInterrupt:
    pass

