# import necessary dependencies
import os, serial, time

# create serial port object
ser = serial.Serial()

# specify serial port on the device
ser.port = "/dev/serial0"

# specify baudrate of the port
# remember to do so also on the hardware (stty)
ser.baudrate = 230400

# specify 8 bits per bytes UART
ser.bytesize = serial.EIGHTBITS

# set parity check: odd parity
ser.parity = serial.PARITY_ODD

# specify number of stop bits
ser.stopbits = serial.STOPBITS_ONE

# disable software flow control
ser.xonxoff = False

# disable hardware (RTS/CTS) flow control
ser.rtscts = False

# disable hardware (DSR/DTR) flow control
ser.dsrdtr = False

# none blocking write
ser.write_timeout = None

try:
    # open serial port
    ser.open()

except Exception as ex:
    # mitigate error opening port
    print("[ALERT] Exception opening:", ex)

    exit()

if ser.is_open:

    try:

        # flush output buffer, discard buffer contents
        ser.reset_output_buffer()

        # timer: get ready for the write i.e., move your shadow
        time.sleep(5)

        print('[INFO] Starting ...')

        ## context manager: open transmission file for reading
        with open('input.txt', 'r') as infile:

            # encode file contents
            text = infile.read().encode('utf-8')

            # count bytes to be transmitted
            text_bytes = len(text)

            # log start time
            start = time.time()

            # write contents
            ser.write(text)

            print('[INFO] Done')

            # log stop time
            stop = time.time()

            # calculate transmission duration
            duration = stop - start

            print('              SUMMARY               ')
            print('------------------------------------')
            print("Time",duration)

            print("Bytes",text_bytes)

            print("Rate (Bps)",text_bytes/duration)

    except Exception as ex:
        # mitigate error communicating via port
        print("[ALERT] Exception communicating:", ex)

    finally:
        # always close port after transmission
        ser.close()

else:

        print("[ALERT] Cannot open serial port!")
