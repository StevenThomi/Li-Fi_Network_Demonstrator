##################################################################
#~~~~~~~~~~~~~~~~~~~~~AMPLITUDE SHIFT KEYING~~~~~~~~~~~~~~~~~~~~~#
# Objectives: (1) convert file to bitstream                      #
#             (2) represent file as a high or low value          #
#~~~~~~~~~AUTHOR: STEVE THOMI <THMSTE021@myuct.ac.za>~~~~~~~~~~~~#
##################################################################

## import the necessary packages
import os
import RPi.GPIO as GPIO
import sys
import time

## read_file method
# @param file_name file to read from [.txt,]
# Objective: (1) open specified file
# (2) extract and return contents
def read_file(file_name="text.txt"):
    # ensure file exists in current working directory
    if os.path.isfile(file_name):
        # ensure file is of type .txt
        if os.path.splitext(file_name)[1]==".txt":
            ## context: open file_name for reading
            with open(file_name, "r") as file:
                ## return file contents
                return file.read().strip()

## encode method
# @param text characters to encode
# Objective: (1) split text into words
# (2) extract and return contents
def encode(text):
    ## clock period T = 2*WAIT
    WAIT = 0.001
    # create list of words from text
    words = text.split()

    # log start time
    start = time.time()
    for word in words:
        # for every word in the words list do ...
        for ch in word:
            # for every character in a word do ...
            ## obtain representative ascii code
            try:
                asc = ord(ch)
            except:
                sys.exit(f"Exception: {asc} not found in ASCII table")
            fill = 8 - asc.bit_length()
            ## represent char as 8 bit ascii
            bits = "0"*fill + bin(asc)[2:]

            for b in bits:
                # for every bit in the ascii do ...
                if b == "1":
                    pwm.start(100)
                else:
                    pwm.ChangeDutyCycle(0)

            time.sleep(WAIT)
        gpio_space(WAIT)

    print(f"Time span: {time.time()-start}")

## gpio_space method
# @param WAIT half clock period
# Objective: (1) flash [SPACE] ascii
# (2) extract and return contents
def gpio_space(WAIT):
    pwm.ChangeDutyCycle(0)
    time.sleep(WAIT*2)
    pwm.start(100)
    time.sleep(WAIT)
    pwm.ChangeDutyCycle(0)
    time.sleep(WAIT*5)

## main method
def main():
    ## I/O config
    print("[INFO] GPIO 13 (pin 33) used as output pin.")

    print("[INFO] reading file...")
    text = read_file()

    print("[INFO] encoding text...")
    encode(text)

    ## Deallocate RPi resources
    pwm.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    ## Raspberry Pi config
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(13, GPIO.OUT)
    pwm = GPIO.PWM(13, 50)
    main()
