# Petworks

Creating a Raspberry Pi-based digital pet with the purpose of helping in preventing RSI specifically for Digital artists. 
The pet has both a physical and virtual presence.

---

### Electronics Code

For the pets hardware functionality, it includes motion sensor for the pet to know when it has been picked up and  a 
vibration motor that allows the pet to vibrate as a result of knowing when it has been picked up.
For this I used the Enviro pHat sensing board as it has a motion sensor (accelerometer/magnetometer) and two white LEDs
which is what I will be primarily using for my Pet.

https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-phat

From the Documentation found on Pimoroni, the following was sampled for my code

### Installing the software
```
curl https://get.pimoroni.com/envirophat | bash
```
---

### Light

```
from envirophat import leds
leds.on()

leds.off()
```

### Motion
```
from envirophat import motion

x, y, z = motion.accelerometer()
print(x, y, z)

import time

while True:
    print(motion.accelerometer())
    time.sleep(0.1)
    
print(motion.heading())

north = motion.heading()

corr_heading = (motion.heading() - north) % 360
print(corr_heading)
```
---

### Logging values

```
import time
from envirophat import light, motion, weather, leds

out = open('enviro.log', 'w')
out.write('light\trgb\tmotion\theading\ttemp\tpress\n')

try:
    while True:
        lux = light.light()
        leds.on()
        rgb = str(light.rgb())[1:-1].replace(' ', '')
        leds.off()
        acc = str(motion.accelerometer())[1:-1].replace(' ', '')
        heading = motion.heading()
        temp = weather.temperature()
        press = weather.pressure()
        out.write('%f\t%s\t%s\t%f\t%f\t%f\n' % (lux, rgb, acc, heading, temp, press))
        time.sleep(1)

except KeyboardInterrupt:
    leds.off()
    out.close()
```

### Timestamp

```
import datetime

timestamp = datetime.datetime.now().isoformat()
```

---
Focusing on making the vibration motor working first, as shown in the code below

### Vibration Motor

```
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

print ("Vibration On")
GPIO.output(18,GPIO.HIGH)

time.sleep(0.5)

print ("Vibration Off")

GPIO.output(18,GPIO.LOW)

```
Then making the Enviro pHat Motion Sensor work, as shown in the code below
### Motion Sensor

```
import time

from envirophat import motion, leds

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
        else:
            print("Motion UnDetected")
            leds.off()

except KeyboardInterrupt:
    pass
```

### Final Code

Combined both the Vibration Motor code and the Motion Sensor Code

```
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
```

For the Data Logging, The pet would log the amount of time that it is spent being held 
and this would be visualised for the web presence of the pet. 


