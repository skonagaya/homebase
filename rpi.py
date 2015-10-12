DEBUG_ENABLED = False

import web
import json
import random
import time
import shelve
import string
import RPi.GPIO as GPIO
import sys
import threading
import memcache
import os
import datetime
import pytz 				# used to localize astral datetime objects
from pytz import timezone	# set timezone to native datetime objects
from astral import Astral 	# compute sunset datetime


#sys.stdout = open('catalina.out', 'a')
#sys.stderr = open('catalina.out', 'a')

clearScreen = lambda: os.system('clear')
clearScreen()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


remoteWaitTime = 2
pirWaitTime = 1
timerWaitTime = 5

timerDeltaThreshold = 15
 
channel1On = 4
channel1Off = 17
channel2On = 9
channel2Off = 23
channel3On = 7
channel3Off = 11

pirOn = 10

pir_pin = 22

print "Setting up GPIO pins ...", 
GPIO.setup(channel1On, GPIO.OUT)
GPIO.setup(channel1Off, GPIO.OUT)
GPIO.setup(channel2On, GPIO.OUT)
GPIO.setup(channel2Off, GPIO.OUT)
GPIO.setup(channel3On, GPIO.OUT)
GPIO.setup(channel3Off, GPIO.OUT)
GPIO.setup(pirOn, GPIO.OUT)
GPIO.setup(pir_pin, GPIO.IN)
print "done."

print "Setting up Astral package ...",
geo = Astral()
SUNSET = geo['San Francisco']
print "done."

print "Allocating memcache ...",
mc = memcache.Client([('127.0.0.1', 11211)])
print "done."

print "Initializing web application library ...",
urls = ('/', 'tutorial')
render = web.template.render('templates/')
app = web.application(urls, globals())
print "done."

def stringToDatetime(frontendTime):
	frontendTime = frontendTime.strip().split(":")
	hour = int(frontendTime[0])
	minute = int(frontendTime[1])
	frontendTime = datetime.time(hour,minute,0,0)
	backendTime = datetime.datetime.combine(datetime.datetime.today(),frontendTime)
	return backendTime


def initmem(memclient):
	if memclient.get("ch1") == "1":
		time.sleep(remoteWaitTime)
		turnOff(1,memclient)

	if memclient.get("ch2") == "1":
		time.sleep(remoteWaitTime)
		turnOff(2,memclient)

	if memclient.get("ch3") == "1":
		time.sleep(remoteWaitTime)
		turnOff(3,memclient)

	if memclient.get("pir") == "1":
		time.sleep(remoteWaitTime)
		turnOff(4,memclient)

	if memclient.get("ch1on")  == None:	turnOnTimer (1,"0",memclient)
	if memclient.get("ch1off") == None:	turnOffTimer(1,"0",memclient)
	if memclient.get("ch2on")  == None:	turnOnTimer (2,"0",memclient)
	if memclient.get("ch2off") == None:	turnOffTimer(2,"0",memclient)
	if memclient.get("ch3on")  == None:	turnOnTimer (3,"0",memclient)
	if memclient.get("ch3off") == None:	turnOffTimer(3,"0",memclient)
	if memclient.get("piron")  == None:	turnOnTimer (4,"0",memclient)
	if memclient.get("piroff") == None:	turnOffTimer(4,"0",memclient)

def turnOnTimer(channel,setTime,memclient):
	if   channel == 1: memclient.set("ch1on", setTime)
	elif channel == 2: memclient.set("ch2on", setTime)
	elif channel == 3: memclient.set("ch3on", setTime)
	elif channel == 4: memclient.set("piron", setTime)

def turnOffTimer(channel,setTime,memclient):
	if   channel == 1: memclient.set("ch1off", setTime)
	elif channel == 2: memclient.set("ch2off", setTime)
	elif channel == 3: memclient.set("ch3off", setTime)
	elif channel == 4: memclient.set("piroff", setTime)

def turnOn(channel,memclient):
	if DEBUG_ENABLED: print "["+time.strftime("%c")+"]" + " Turning on channel " + str(channel) 
	if channel == 1:
		GPIO.output(channel1On, 1)
		time.sleep(remoteWaitTime)
		GPIO.output(channel1On, 0)
		memclient.set("ch1", "1")
	elif channel == 2:
		GPIO.output(channel2On, 1)
		time.sleep(remoteWaitTime)
		GPIO.output(channel2On, 0)
		memclient.set("ch2", "1")
	elif channel == 3:
		GPIO.output(channel3On, 1)
		time.sleep(remoteWaitTime)
		GPIO.output(channel3On, 0)
		memclient.set("ch3", "1")
	elif channel == 4:
		GPIO.output(pirOn, 1)
		memclient.set("pir", "1")
	time.sleep(remoteWaitTime)


def turnOff(channel,memclient):
	if DEBUG_ENABLED: print "["+time.strftime("%c")+"]" + " Turning off channel " + str(channel)
	if channel == 1:
		GPIO.output(channel1Off, 1)
		time.sleep(remoteWaitTime)
		GPIO.output(channel1Off, 0)
		memclient.set("ch1", "0")
	elif channel == 2:
		GPIO.output(channel2Off, 1)
		time.sleep(remoteWaitTime)
		GPIO.output(channel2Off, 0)
		memclient.set("ch2", "0")
	elif channel == 3:
		GPIO.output(channel3Off, 1)
		time.sleep(remoteWaitTime)
		GPIO.output(channel3Off, 0)
		memclient.set("ch3", "0")
	elif channel == 4:
		GPIO.output(pirOn, 0)
		memclient.set("pir", "0")
	time.sleep(remoteWaitTime)

def timeElapsedSince(thisTime):
	elapsed_time = time.time() - thisTime
	return elapsed_time

def memToDict(memclient):
	toDict = {}
	toDict["ch1"] = memclient.get("ch1")
	toDict["ch2"] = memclient.get("ch2")
	toDict["ch3"] = memclient.get("ch3")
	toDict["pir"] = memclient.get("pir")

	toDict["ch1on"] = memclient.get("ch1on")
	toDict["ch2on"] = memclient.get("ch2on")
	toDict["ch3on"] = memclient.get("ch3on")
	toDict["piron"] = memclient.get("piron")

	toDict["ch1off"] = memclient.get("ch1off")
	toDict["ch2off"] = memclient.get("ch2off")
	toDict["ch3off"] = memclient.get("ch3off")
	toDict["piroff"] = memclient.get("piroff")


	if DEBUG_ENABLED: print "The List:",
	if DEBUG_ENABLED: print toDict

	print toDict
	return toDict

class tutorial:
	def GET(self):
		return render.tutorial()

	def POST(self):
		if DEBUG_ENABLED: print "["+time.strftime("%c")+"]" + " Received POST: "
		web.header('Content-Type', 'application/json')
		channel = web.input()["channel"].strip()
		state = web.input()["state"].strip()
		mode = web.input()["mode"].strip()
		#print "\tCMD \""+cmd+"\""
		#print "\tSTATE \""+state+"\""
		mem = memcache.Client([('127.0.0.1', 11211)])
		if mode == "toggle":
			if channel == "ch1":
				if state == "on": turnOn(1,mem)
				elif state == "off": turnOff(1,mem)
				return json.dumps({"id":"ch1"})
			elif channel == "ch2":
				if state == "on": turnOn(2,mem)
				elif state == "off": turnOff(2,mem)
				return json.dumps({"id":"ch2"})
			elif channel == "ch3":
				if state == "on": turnOn(3,mem)
				elif state == "off": turnOff(3,mem)
				return json.dumps({"id":"ch3"})
			elif channel == "pir":
				if state == "on": turnOn(4,mem)
				elif state == "off": turnOff(4,mem)
				return json.dumps({"id":"pir"})
		elif mode == "signal":
			if channel == "volumeup":
				os.system('irsend SEND_ONCE rpi KEY_VOLUMEUP')
				os.system('irsend SEND_ONCE rpi KEY_VOLUMEUP')
				os.system('irsend SEND_ONCE rpi KEY_VOLUMEUP')
				os.system('irsend SEND_ONCE rpi KEY_VOLUMEUP')
				os.system('irsend SEND_ONCE rpi KEY_VOLUMEUP')
			elif channel == "volumedown":
				os.system('irsend SEND_ONCE rpi KEY_VOLUMEDOWN')
				os.system('irsend SEND_ONCE rpi KEY_VOLUMEDOWN')
				os.system('irsend SEND_ONCE rpi KEY_VOLUMEDOWN')
				os.system('irsend SEND_ONCE rpi KEY_VOLUMEDOWN')
				os.system('irsend SEND_ONCE rpi KEY_VOLUMEDOWN')
			elif channel == "receiveron":
				os.system('irsend SEND_ONCE rpi KEY_POWER')
			elif channel == "receiveroff":
				os.system('irsend SEND_ONCE rpi KEY_SLEEP')
			elif channel == "tv":
				os.system('irsend SEND_ONCE rpi KEY_POWER2')
		elif mode == "timer":
			setTime = web.input()["time"].strip()
			if channel == "ch1on":
				if state == "on": 
					turnOnTimer(1,setTime,mem)
					return json.dumps({"id":"ch1on","result":"on"})
				elif state == "off": 
					turnOnTimer(1,"0",mem)
					return json.dumps({"id":"ch1on","result":"off"})
			elif channel == "ch2on":
				if state == "on": 
					turnOnTimer(2,setTime,mem)
					return json.dumps({"id":"ch2on","result":"on"})
				elif state == "off": 
					turnOnTimer(2,"0",mem)
					return json.dumps({"id":"ch2on","result":"off"})
			elif channel == "ch3on":
				if state == "on": 
					turnOnTimer(3,setTime,mem)
					return json.dumps({"id":"ch3on","result":"on"})
				elif state == "off": 
					turnOnTimer(3,"0",mem)
					return json.dumps({"id":"ch3on","result":"off"})
			elif channel == "piron":
				if state == "on": 
					turnOnTimer(4,setTime,mem)
					return json.dumps({"id":"piron","result":"on"})
				elif state == "off": 
					turnOnTimer(4,"0",mem)
					return json.dumps({"id":"piron","result":"off"})
			elif channel == "ch1off":
				if state == "on": 
					turnOffTimer(1,setTime,mem)
					return json.dumps({"id":"ch1off","result":"on"})
				elif state == "off": 
					turnOffTimer(1,"0",mem)
					return json.dumps({"id":"ch1off","result":"off"})
			elif channel == "ch2off":
				if state == "on": 
					turnOffTimer(2,setTime,mem)
					return json.dumps({"id":"ch2off","result":"on"})
				elif state == "off": 
					turnOffTimer(2,"0",mem)
					return json.dumps({"id":"ch2off","result":"off"})
			elif channel == "ch3off":
				if state == "on": 
					turnOffTimer(3,setTime,mem)
					return json.dumps({"id":"ch3off","result":"on"})
				elif state == "off": 
					turnOffTimer(3,"0",mem)
					return json.dumps({"id":"ch3off","result":"off"})
			elif channel == "piroff":
				if state == "on": 
					turnOffTimer(4,setTime,mem)
					return json.dumps({"id":"piroff","result":"on"})
				elif state == "off": 
					turnOffTimer(4,"0",mem)
					return json.dumps({"id":"piroff","result":"off"})
		elif mode == "check":
			if DEBUG_ENABLED: print "\tSending all channel states"
			return json.dumps(memToDict(mem))
		#result = json.dumps("channel 1 complete")
		return None

class TimerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while True:
			ch1on  = mc.get("ch1on")
			ch2on  = mc.get("ch2on")
			ch3on  = mc.get("ch3on")
			piron  = mc.get("piron")
			ch1off = mc.get("ch1off")
			ch2off = mc.get("ch2off")
			ch3off = mc.get("ch3off")
			piroff = mc.get("piroff")

			currentTime = datetime.datetime.now()

			if ch1on != "0":
				if DEBUG_ENABLED: print "ch1on: " + ch1on
				timeLeft = (currentTime - stringToDatetime(ch1on)).total_seconds()
				if DEBUG_ENABLED: print "TimeLeft: " + str(timeLeft)
				if timeLeft > 0 and timeLeft < timerDeltaThreshold:
					turnOn(1,mc)
			if ch2on != "0":
				if DEBUG_ENABLED: print "ch2on: " + ch2on
				timeLeft = (currentTime - stringToDatetime(ch2on)).total_seconds()
				if DEBUG_ENABLED: print "TimeLeft: " + str(timeLeft)
				if timeLeft > 0 and timeLeft < timerDeltaThreshold:
					turnOn(2,mc)
			if ch3on != "0":
				if DEBUG_ENABLED: print "ch3on: " + ch3on
				timeLeft = (currentTime - stringToDatetime(ch3on)).total_seconds()
				if DEBUG_ENABLED: print "TimeLeft: " + str(timeLeft)
				if timeLeft > 0 and timeLeft < timerDeltaThreshold:
					turnOn(3,mc)
			if piron != "0":
				if DEBUG_ENABLED: print "piron: " + piron
				timeLeft = (currentTime - stringToDatetime(piron)).total_seconds()
				if DEBUG_ENABLED: print "TimeLeft: " + str(timeLeft)
				if timeLeft > 0 and timeLeft < timerDeltaThreshold:
					turnOn(4,mc)

			if ch1off != "0":
				if DEBUG_ENABLED: print "ch1off: " + ch1off
				timeLeft = (currentTime - stringToDatetime(ch1off)).total_seconds()
				if DEBUG_ENABLED: print "TimeLeft: " + str(timeLeft)
				if timeLeft > 0 and timeLeft < timerDeltaThreshold:
					turnOff(1,mc)
			if ch2off != "0":
				if DEBUG_ENABLED: print "ch2off: " + ch2off
				timeLeft = (currentTime - stringToDatetime(ch2off)).total_seconds()
				if DEBUG_ENABLED: print "TimeLeft: " + str(timeLeft)
				if timeLeft > 0 and timeLeft < timerDeltaThreshold:
					turnOff(2,mc)
			if ch3off != "0":
				if DEBUG_ENABLED: print "ch3off: " + ch3off
				timeLeft = (currentTime - stringToDatetime(ch3off)).total_seconds()
				if DEBUG_ENABLED: print "TimeLeft: " + str(timeLeft)
				if timeLeft > 0 and timeLeft < timerDeltaThreshold:
					turnOff(3,mc)
			if piroff != "0":
				if DEBUG_ENABLED: print "piroff: " + piroff
				timeLeft = (currentTime - stringToDatetime(piroff)).total_seconds()
				if DEBUG_ENABLED: print "TimeLeft: " + str(timeLeft)
				if timeLeft > 0 and timeLeft < timerDeltaThreshold:
					turnOff(4,mc)

			#print "Tick Tock: sleeping for: " + str(timerWaitTime)
			time.sleep(timerWaitTime)



class MotionSensorThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def motionActionOn(self):
		print "******* IN MOTION ACTION ON *******"
		#os.system('irsend SEND_ONCE rpi KEY_POWER2') 		#TOGGLE TV

		os.system('irsend SEND_START rpi KEY_POWER2') 	#LOWER VOLUME
		time.sleep(0.5)
		os.system('irsend SEND_STOP rpi KEY_POWER2') 	#LOWER VOLUME
		time.sleep(1)
		os.system('irsend SEND_ONCE rpi KEY_POWER') 		#TURN ON RECEIVER

		time.sleep(10)

		print "**** STARTING VOLUME DOWN SEQUENCE ****"

		for i in range(0, 41): os.system('irsend SEND_ONCE rpi KEY_VOLUMEDOWN') 	#LOWER VOLUME

		
		#os.system('irsend SEND_START rpi KEY_VOLUMEDOWN') 	#LOWER VOLUME
		#time.sleep(1.6)
		#os.system('irsend SEND_STOP rpi KEY_VOLUMEDOWN') 	#LOWER VOLUME


	def motionActionOff(self):
		print "******* IN MOTION ACTION OFF *******"
		#os.system('irsend SEND_ONCE rpi KEY_POWER2') 		#TOGGLE TV
		os.system('irsend SEND_START rpi KEY_POWER2') 	#LOWER VOLUME
		time.sleep(0.5)
		os.system('irsend SEND_STOP rpi KEY_POWER2') 	#LOWER VOLUME
		time.sleep(1)
		os.system('irsend SEND_ONCE rpi KEY_SLEEP')


		'''
	### CODE FOR EMITTING CODE THROUGH IR LED
	def run(self):
		IDLE_SECONDS_ALLOWED = 2
		timeOn = 0
		waitingForTimeOut = False
		onState = False

		while True:
			if waitingForTimeOut:
				print timeElapsedSince(timeOn)
				if timeElapsedSince(timeOn) > IDLE_SECONDS_ALLOWED: #IF IDLE
					waitingForTimeOut = False
					timeOn = 0
			if GPIO.input(pir_pin):
				print "["+time.strftime("%c")+"]" + " Motion Detected "
				waitingForTimeOut = True
				if timeOn == 0:
					if onState:
						self.motionActionOff()
						onState = False
						print "Detected On State, now turning off"
					elif not onState:
						self.motionActionOn()
						onState = True
						print "Detected Off State, now turning on"
				timeOn = time.time()
			time.sleep(pirWaitTime)
		return
	###CODE FOR TURNING ON AND OFF A CHANNEL WITH A IDLE TIMEOUT
	def run(self):
		IDLE_SECONDS_ALLOWED = 360
		timeOn = 0

		while True:
			if "1" in mc.get("ch1"):
				#print timeElapsedSince(timeOn)
				if timeElapsedSince(timeOn) > IDLE_SECONDS_ALLOWED: #IF IDLE
					turnOff(1,mc)
					timeOn = 0
			if GPIO.input(pir_pin):
				print "["+time.strftime("%c")+"]" + " Motion Detected "
				print mc.get("ch1")
				timeOn = time.time()
				if "0" in mc.get("ch1"): 
					turnOn(1,mc)
			time.sleep(pirWaitTime)
		return

		''' 
	###CODE FOR TURNING ON AND OFF A CHANNEL WITH A SUNSET TIMEOUT
	def run(self):
		IDLE_SECONDS_ALLOWED = 360

		while True:
			if mc.get("pir"):
				if GPIO.input(pir_pin): 										#If data is streaming from our PIR pin
					print "["+time.strftime("%c")+"]" + " Motion Detected "
					print mc.get("ch1")

					cutoffHour 	= 22 #PM
					cutoffMin	=  0
					cutoffSec	=  0
					cutoffMs	=  0

					cutoffDatetime = datetime.datetime.now(timezone('US/Pacific')).replace(
						hour=cutoffHour,
						minute=cutoffMin,
						second=cutoffSec,
						microsecond=cutoffMs)

					sunsetDatetime = SUNSET.sun(date=datetime.datetime.now(),local=True)['sunset']
					currentDatetime = datetime.datetime.now(timezone('US/Pacific'))

					if DEBUG_ENABLED: print "Cutoff: " +str(cutoffDatetime)
					if DEBUG_ENABLED: print "Currnt: " +str(currentDatetime)
					if DEBUG_ENABLED: print "Sunset: " +str(sunsetDatetime) + "\n"

					if currentDatetime > sunsetDatetime and currentDatetime < cutoffDatetime:
						print "Motion Detected in sunset window"
						if "0" in mc.get("ch1"): 
							print "Turning on since motion was detected"
							turnOn(1,mc)

			time.sleep(pirWaitTime)
		return


if __name__ == '__main__':
	print "Initiating memcache data ...",
	initmem(mc)
	print "done."
	print "Starting motion thread ...",
	mst = MotionSensorThread()
	mst.start()
	print "done."
	print "Starting main thread ...",
	tt = TimerThread()
	tt.start()
	print "done."
	print "\n\t[!] SYSTEM ONLINE\n"
	app.run()
