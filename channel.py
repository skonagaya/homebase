import RPi.GPIO as GPIO
import time
import datetime
 
GPIO.setmode(GPIO.BCM)
 
pin4 = 4
pin17 = 17
pin9 = 9
pin23 = 23
pin7 = 7
pin11 = 11
pin21 = 10

pir_pin = 22
isOn = False
timeOne = None
IDLE_SECONDS_ALLOWED = 120
 
GPIO.setup(pin4, GPIO.OUT)
GPIO.setup(pin17, GPIO.OUT)
GPIO.setup(pin9, GPIO.OUT)
GPIO.setup(pin23, GPIO.OUT)
GPIO.setup(pin7, GPIO.OUT)
GPIO.setup(pin11, GPIO.OUT)
GPIO.setup(pin21, GPIO.OUT)

GPIO.setup(pir_pin, GPIO.IN)

def testAll():
	GPIO.output(pin4,  0)
	GPIO.output(pin17, 0)
	GPIO.output(pin9,  0)
	GPIO.output(pin23, 0)
	GPIO.output(pin7,  0)
	GPIO.output(pin11, 0)

	time.sleep(0.5)

	GPIO.output(pin4,  1)
	time.sleep(0.5)
	GPIO.output(pin4,  0)

	time.sleep(0.5)

	GPIO.output(pin17, 1)
	time.sleep(0.5)
	GPIO.output(pin17, 0)

	time.sleep(0.5)

	GPIO.output(pin9,  1)
	time.sleep(0.5)
	GPIO.output(pin9,  0)

	time.sleep(0.5)

	GPIO.output(pin23, 1)
	time.sleep(0.5)
	GPIO.output(pin23, 0)

	time.sleep(0.5)

	GPIO.output(pin7, 1)
	time.sleep(0.5)
	GPIO.output(pin7, 0)

	time.sleep(0.5)

	GPIO.output(pin11, 1)
	time.sleep(0.5)
	GPIO.output(pin11, 0)

	time.sleep(0.5)

	GPIO.output(pin21, 1)
	time.sleep(0.5)
	GPIO.output(pin21, 0)

def timeElapsedSince(thisTime):
	elapsed_time = time.time() - thisTime
	return elapsed_time

while True:

	if isOn:
		print timeElapsedSince(timeOn)
		if timeElapsedSince(timeOn) > IDLE_SECONDS_ALLOWED:
			print "TURNING OFF"
			isOn = False
			timeOne = 0
	if GPIO.input(pir_pin):
		timeOn = time.time()
		if not isOn:
        		print "TURNING ON"
			isOn = True
	time.sleep(0.5)

	if True:
		input = raw_input("on or off?")
		if input.lower().strip() == "on1":
			GPIO.output(pin4, 1)
	        elif input.lower().strip() == "off1":
	                GPIO.output(pin4, 0)
	        elif input.lower().strip() == "on2":
	                GPIO.output(pin17, 1)
	        elif input.lower().strip() == "off2":
	                GPIO.output(pin17, 0)
	        elif input.lower().strip() == "on3":
	                GPIO.output(pin9, 1)
	        elif input.lower().strip() == "off3":
	                GPIO.output(pin9, 0)
	        elif input.lower().strip() == "on4":
	                GPIO.output(pin23, 1)
	        elif input.lower().strip() == "off4":
	                GPIO.output(pin23, 0)
	        elif input.lower().strip() == "on5":
	                GPIO.output(pin7, 1)
	        elif input.lower().strip() == "off5":
	                GPIO.output(pin7, 0)
	        elif input.lower().strip() == "on6":
	                GPIO.output(pin11, 1)
	        elif input.lower().strip() == "off6":
	                GPIO.output(pin11, 0)
	        elif input.lower().strip() == "on7":
	                GPIO.output(pin21, 1)
	        elif input.lower().strip() == "off7":
	                GPIO.output(pin21, 0)
		elif input.lower().strip() == "all":
			testAll()


