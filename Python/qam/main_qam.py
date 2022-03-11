##################################################################
#~~~~~~~~~~~~~~~~~QUADRATURE AMPLITUDE MODULATION~~~~~~~~~~~~~~~~#
# Objectives: (1) convert file to bitstream                      #
#             (2) represent file as a series of qam symbols      #
#~~~~~~~~~AUTHOR: STEVE THOMI <THMSTE021@myuct.ac.za>~~~~~~~~~~~~#
##################################################################

## import the necessary packages
import concurrent.futures as mp
import numpy as np
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
    # time domain output list
    x = []
    bits = ""

    # log start time
    # start = time.time()
    for word in words:
        # for every word in the words list do ...
        for ch in word:
            ## obtain representative ascii code
            # for every character in a word do ...
            try:
                asc = ord(ch)
            except:
                sys.exit(f"Exception: {asc} not found in ASCII table")
            fill = 8 - asc.bit_length()
            ## represent char as 8 bit ascii
            bits += "0"*fill + bin(asc)[2:]

    # context parallel create to process bitstream
    with mp.ProcessPoolExecutor() as executor:
        # process the bitstream in byte-wide chunks
        for i in range(0,len(bits),8):
            results = executor.map(serial_to_parallel,[bits[i:i+4],bits[i+4:i+8]])

            # apply Hermitian symmetry to half the transmitted data
            for result in results:
                x.append(result[:2])

    ## add a DC offset equal to the signal average
    x_dc = [i+1.25 for i in x]
    ## derive the pwm output sequence
    pwm_dc = [k/2.5*100 for k in x_dc]

    ## display the pwm output sequence
    for p in pwm_dc:
        for q in p:
            pwm.ChangeDutyCycle(q)
            time.sleep(WAIT)

    # print(f"Time span: {time.time()-start}")

## serial_to_parallel method
# @param bit_stream bit sequence representation
# Objective: (1) match bitstream to qam representation
# (3) compute ifft of real time dom. signal
# (2) return ifft
def serial_to_parallel(bit_stream):
    X = qam_map(bit_stream)
    return np.fft.irfft(X)

## qam_map method
# @param bit_stream bit sequence representation
# Objective: (1) match bitstream to qam representation
def qam_map(bit_stream):
    if bit_stream == "0000":
        return [0,2.5 + 2.5j,0]
    elif bit_stream == "0001":
        return [0,2.5 - 2.5j,0]
    elif bit_stream == "0010":
        return [0,2.5 + 1.5j,0]
    elif bit_stream == "0011":
        return [0,2.5 - 1.5j,0]
    elif bit_stream == "0100":
        return [0,-2.5 + 2.5j,0]
    elif bit_stream == "0101":
        return [0,-2.5 - 2.5j,0]
    elif bit_stream == "0110":
        return [0,-2.5 + 1.5j,0]
    elif bit_stream == "0111":
        return [0,-2.5 - 1.5j,0]
    elif bit_stream == "1000":
        return [0,1.5 + 2.5j,0]
    elif bit_stream == "1001":
        return [0,1.5 - 2.5j,0]
    elif bit_stream == "1010":
        return [0,1.5 + 1.5j,0]
    elif bit_stream == "1011":
        return [0,1.5 - 1.5j,0]
    elif bit_stream == "1100":
        return [0,-1.5 + 2.5j,0]
    elif bit_stream == "1101":
        return [0,-1.5 - 2.5j,0]
    elif bit_stream == "1110":
        return [0,-1.5 + 1.5j,0]
    elif bit_stream == "1111":
        return [0,-1.5 - 1.5j,0]
    else:
        return [0,2.5 + 2.5j,0]

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
    pwm.start(0)
    main()
