import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

comp = 4
troyka = 17
dac = [26, 19, 13, 6, 5, 11, 9, 10]

for i in dac: GPIO.setup(i, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(elem) for elem in bin(value)[2:].zfill(8)]

def adc():
    ret = 0
    value = 0
    for j in range(7, -1 , -1):
        value = ret + 2**j
        binlist = dec2bin(value)
        for i in range(len(dac)): GPIO.output(dac[i], binlist[i])
        time.sleep(0.001)
        if GPIO.input(comp) == 1: ret += 2**j
    return ret

try:
    while True:
        value = adc()
        print(value, "{:.3}".format(3.3 * value / 256))


finally:
    for i in dac: GPIO.output(i, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup() 