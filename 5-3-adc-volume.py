import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

comp = 4
troyka = 17
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]

for i in dac: GPIO.setup(i, GPIO.OUT)
for j in leds: GPIO.setup(j, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(elem) for elem in bin(value)[2:].zfill(8)]

def adc():
    for value in range(256):
        binlist = dec2bin(value)
        for i in range(len(dac)): GPIO.output(dac[i], binlist[i])
        time.sleep(0.001)
        if GPIO.input(comp) == 0: return value

try:
    while True:
        value = adc()
        print(value, "{:.3}".format(3.3 * value / 256))
        ledslist = dec2bin(2**(round(8*value/256))-1)
        for k in range(len(leds)): GPIO.output(leds[k], ledslist[k])


finally:
    for i in dac: GPIO.output(i, 0)
    for i in leds: GPIO.output(i, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup() 