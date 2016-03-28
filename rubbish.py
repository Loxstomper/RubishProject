import RPi.GPIO as GPIO
import time
import os
import random
import subprocess
import socket


# variables
rubbish_time = ''


# server
hostname = 'localhost'
port = '5555'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# GPIO
GPIO.setwarnings(False)  # disables warnings
GPIO.setmode(GPIO.BCM)  # puts GPIO in correct mode

# pin numbers
TRIG = 23
ECHO = 24


# sounds
sounds = os.listdir('./sounds/')  # creates list of all sound names
totalSounds = len(sounds)
next_sound = ''


# gets value of uses
usesFile = open('uses.txt', 'r')
uses = usesFile.read()
usesFile.close()

# distance
pulseStart = 0
pulseEnd = 0
distance = 0

# condition for loop
soundPlaying = False


# functions

def ui():
    os.system('clear')
    print("Rubbish project by Lochie Ashcroft.")
    print("This project can be found on github.com/loxstomper/RubbishProject/")
    print("\nConnected to server ", hostname)
    print("Connect to http://", hostname, " to view the website.")
    print("There are a total of ", len(sounds), " sounds")
    print("Uses:", uses, "\n")


def trigger_sensor():
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)


def play_sound():
    # get a random sound, - 1 because first element is 0
    sound_number = random.randint(0, (len(sounds) - 1))
    next_sound = str(sounds[sound_number])

    # send next_sound to server

    soundPlaying = True  # top make sure only one sound is played at a time
    subprocess.call(["mpg321", "./sounds/%s" % next_sound])
    soundPlaying = False


def send_to_server(rubbish_time, sound):
    s.send(rubbish_time.encode())
    s.send(str.encode(' '))
    s.send(sound.encode())


# connecting to server
print("Connecting to server @:", hostname, port, "...")
s.connect((hostname, port))
print("Connected successfully")

# splash screen
ui()

while soundPlaying == False:
    initialDistance = distance
    trigger_sensor()

    while GPIO.input(ECHO) == 0:  # record time of the pulse
        pulseStart = time.time()

    while GPIO.input(ECHO) == 1:  # end of pulse
            pulseEnd = time.time()

    # CALCULATING DISTANCE
    pulseDuration = pulseEnd - pulseStart
    distance = pulseDuration * 17150
    distance = round(distance, 2)  # rounded to 2 digits
    # print("Distance: ", distance, "cm")  # remove this for final version

    # if rubbish has been put into the bin
    if distance <= (initialDistance * 0.5):  # less than 50% for tolerance, faster you use the sensor less accurate it is
        uses = int(uses) + 1  # because uses is read from file making it a string

        # send uses to server

        # save uses to file
        usesFile = open('uses.txt', 'w')
        usesFile.write(str(uses))
        usesFile.close()

        # save time of use to file
        usesTime = open('usesTime.txt', 'w')
        usesTime.write(str(time.strftime('%c%n')))  # day month date hour minute second year
        usesTime.close()

        rubbish_time = str(time.strftime('%H:%m:%s'))
        play_sound()
        send_to_server(rubbish_time, next_sound)
        ui()

    time.sleep(0.1)  # wait 1 seconds then repeat

