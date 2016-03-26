import RPi.GPIO as GPIO
import time
import os


GPIO.setwarnings(False)  # disables warnings
GPIO.setmode(GPIO.BCM)  # puts GPIO in correct mode

totalSounds = 100  # will get length of sound list

# gets value of uses
usesFile = open('uses.txt', 'r')
uses = usesFile.read()
usesFile.close()

# GPIO pins
TRIG = 23
ECHO = 24

pulseStart = 0
pulseEnd = 0
distance = 0


def ui():
    os.system('clear')
    print("Rubbish project by Lochie Ashcroft.")
    print("This project can be found on github.com/loxstomper/rubbish/")
    print("\nConnected to server xxx.xxx.x.x")
    print("Connect to xxx.xxx.x.x to view the website.")
    print("Sounds : 5 / 100")
    print("Uses:", uses, "\n")


def trigger_sensor():
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)


while True:
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
    print("Distance: ", distance, "cm")  # remove this for final version

    if distance <= (initialDistance * 0.9):  # less than 90% for tolerance
        uses += 1
        ui()  # redraw ui
        # save uses to file
        usesFile = open('uses.txt', 'w')
        usesFile.write(uses)
        usesFile.close()
        # save time of use to file
        usesTime = open('usesTime', 'w')
        usesTime.write(time.strftime('%c'))  # day month date hour minute second year
        usesTime.close()

