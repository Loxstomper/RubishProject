#!/usr/bin/python3.4.2

import RPi.GPIO as GPIO
import time
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

totalSounds = 100
curSound = 25
#soundsFolder =

usesFile = open("uses.txt", "r")

clearScreen = 0 # once it hits 8 clear screen
distance = 0
uses = 100 #usesFile.read()
TRIG = 23
ECHO = 24

usesFile.close()

# Initial Screen
os.system('clear')
print ("Rubbish project by Lochie Ashcroft & Richard Ngawati")
time.sleep(2)
print ("\n\n[+] Connecting to server")
time.sleep(2) # simulating setting up
print ("	Connected to xxx.xxx.x.x")
time.sleep(1)
print("\n[+] File locations")
print ("	 Number of uses stored in ./uses.txt or uses.csv havent decided yet")
time.sleep(1)
print ("	 Sounds located in ./sounds/")
time.sleep(3)
os.system('clear')
print ("Rubbish project by Lochie Ashcroft & Richard Ngawati.")
print ("This project can be found on github.com/sdfghjklpoiuytrdfghjkjh")
print ("\nConnected to server xxx.xxx.x.x")
print("Connect to xxx.xxx.x.x to view the website.")
print ("Sounds: 5 / 100")#FIX THIS
print ("Uses:"  , uses, "\n") #FIX THIS


# ACTUAL PROGRAM
while True:

		# RESETS SCREEN
		if clearScreen == 14:
			os.system('clear')
			print ("Rubbish project by Lochie Ashcroft & Richard Ngawati.")
			print ("This project can be found on github.com/sdfghjklpoiuytrdfghjkjh")
			print ("\nConnected to server xxx.xxx.x.x")
			print("Connect to xxx.xxx.x.x to view the website.")
			print ("Sounds : 5 / 100")#FIX THIS
			print ("Uses:"   , uses, "\n") #FIX THIS
			clearScreen = 0

		# value for comparing
		initial_distance = distance
	    # Trigger sensor
		GPIO.setup(TRIG, GPIO.OUT)
		GPIO.setup(ECHO, GPIO.IN)
		GPIO.output(TRIG, False)
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)

		while GPIO.input(ECHO)==0: # record time of the pulse
			pulse_start = time.time()

		while GPIO.input(ECHO)==1: # end of pulse
			pulse_end = time.time()

		# CALCULATING DISTANCE
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150 # speed of sound
		distance = round(distance, 2) # rounded to 2 digits

		print ("Distance: ",distance,"cm")
		clearScreen += 1

		if distance <= (initial_distance * 0.9): # 10% less than actual figure just for tolerance
			uses += 1
			usesFile = open("uses.txt", "w")
			usesFile.write(str(uses))
			usesFile.close()
			#os.system('clear')
			#print ("Rubbish project by Lochie Ashcroft & Richard Ngawati.")
			#print ("This project can be found on github.com/sdfghjklpoiuytrdfghjkjh")
			#print ("\nConnected to server xxx.xxx.x.x")
			#print("Connect to xxx.xxx.x.x to view the website.")
			#print ("Sounds : 5 / 100")#FIX THIS
			#print ("Uses:"   , uses) #FIX THIS
		    #clearScreen = 0

		#	usesTime = open("usesTime.txt", "w")
			#usesTime.write((str(time.strftime("%I:%M:%S")))
		#	usesTime.write("\n") # couldnt get new line working above
			#usesTime.close()

			#refresh with everytime it gets tirggered


		time.sleep(1)
