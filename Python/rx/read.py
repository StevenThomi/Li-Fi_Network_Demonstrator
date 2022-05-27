# import necessary dependencies
import serial, datetime

# create serial port object
ser = serial.Serial()   #initialization and open the port

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

# no timeout for read
# read whenever there is something to read
ser.timeout = 0

# disable software flow control
ser.xonxoff = False

# disable hardware (RTS/CTS) flow control
ser.rtscts = False

# disable hardware (DSR/DTR) flow control
ser.dsrdtr = False

# give output file an unique name
file_name = str(datetime.datetime.now())+'.txt'

try:
    # open serial port
    ser.open()

except Exception as ex:
    # mitigate error opening port
    print("[ALERT] Exception opening port:", ex)

    exit()

if ser.isOpen():

    try:
        # flush input buffer, discard buffer contents
        ser.flushInput()

        ## context manager: open output file for writing
        with open(file_name, 'w') as outfile:

            # always loop
            while True:

                # read input buffer,
                # remember timeout = 0, so 32 bytes seek is sufficiently high
                input_text = ser.read(32)

                try:

                    # decode received contents
                    txt = input_text.decode('utf-8')

                except Exception:

                    # if binary, print out the binary as a string
                    txt = str(input_text)

                # if UART receive pin is toggled
                if txt != '':
                    # write to output file
                    outfile.write(txt)

    except Exception as ex:
        # mitigate error communicating via port
        print("[ALERT] Exception communicating:", ex)

    finally:
        # always close port after transmission
        ser.close()

else:

    print("[ALERT] Cannot open serial port!")
