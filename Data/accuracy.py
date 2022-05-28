## import dependencies
from statistics import mean, stdev

## main method
# Objectives:
# - transcribe master file
# - compare test files with master files
def main():
    # list: hold master file transcript
    original_text = list()

    # file array: UART - UART direct connection control environment files
    # control = ['9600_control.txt', '19200_control.txt',
    #                             '38400_control.txt', '57600_control.txt',
    #                             '115200_control.txt', '230400_control.txt',
    #                             '460800_control.txt']

    # dir array: vary UART rate to Li-Fi, well-lit environment
    dark_distance = ['dark_11.25', 'dark_15', 'dark_18.75',
                    'dark_22.5', 'dark_7.5']

    # dir array: vary UART rate to Li-Fi, poorly-lit environment
    light_distance = ['light_11.25', 'light_15', 'light_18.75',
                    'light_22.5', 'light_7.5']

    # dir array: vary LED - Photodiode distance, well-lit environment
    dark_speed = ['dark_115200', 'dark_19200', 'dark_230400',
                'dark_38400', 'dark_460800', 'dark_57600', 'dark_9600']

    # dir array: vary LED - Photodiode distance, poorly-lit environment
    light_speed = ['light_115200', 'light_19200', 'light_230400',
                'light_38400', 'light_460800', 'light_57600', 'light_9600']

    ## context manager: open master file for reading
    with open('master.txt','r') as masterfile:

        for line in masterfile:
            # break each line into words
            arr = line.split()

            for word in arr:
                # check if word is alphanumeric - no symbols i.e., @, \
                if word.isalnum():
                    # add word to transcription if condition is met
                    original_text.append(word)

        print('[INFO] Running tests ...')
        print('             BYTE ERROR RATE SUMMARY            ')
        print('--------------------------------------------------------------------')

        # run accuracy test on varied speed, well-lit environment files
        for dir in light_distance:
            ber_lst = list()
            for i in range(5):
                file = 'light_distance/' + dir + f'/reading_{i+1}.txt'
                ber = run(file, original_text)
                ber_lst.append(ber)

                # pretty output
                print(file, (45 - len(file))*' ',"|\t", round(ber,7))
                print('--------------------------------------------------------------------')

            # pretty output
            print("Mean", round(mean(ber_lst),7),"\t|\t", "Std. Dev", \
                    round(stdev(ber_lst),7))
            print('--------------------------------------------------------------------')
            print()

        # run accuracy test on varied speed, poorly-lit environment files
        for dir in dark_speed:
            ber_lst = list()
            for i in range(5):
                file = 'dark_speed/' + dir + f'/reading_{i+1}.txt'
                ber = run(file, original_text)
                ber_lst.append(ber)

                # pretty output
                print(file, (50 - len(file))*' ',"|\t", round(ber,7))
                print('--------------------------------------------------------------------')

            # pretty output
            print("Mean", round(mean(ber_lst),7),"\t|\t", "Std. Dev", \
                    round(stdev(ber_lst),7))
            print('--------------------------------------------------------------------')

        # run accuracy test on varied distance, well-lit environment files
        for dir in light_speed:
            ber_lst = list()
            for i in range(5):
                file = 'light_speed/' + dir + f'/reading_{i+1}.txt'
                ber = run(file, original_text)
                ber_lst.append(ber)

                # pretty output
                print(file, (50 - len(file))*' ',"|\t", round(ber,7))
                print('--------------------------------------------------------------------')

            # pretty output
            print("Mean", round(mean(ber_lst),7),"\t|\t", "Std. Dev", \
                    round(stdev(ber_lst),7))
            print('--------------------------------------------------------------------')

        # run accuracy test on varied distance, poorly-lit environment files
        for dir in dark_distance:
            ber_lst = list()
            for i in range(5):
                file = 'dark_distance/' + dir + f'/reading_{i+1}.txt'
                ber = run(file, original_text)
                ber_lst.append(ber)

                # pretty output
                print(file, (50 - len(file))*' ',"|\t", round(ber,7))
                print('--------------------------------------------------------------------')

            # pretty output
            print("Mean", round(mean(ber_lst),7),"\t|\t", "Std. Dev", \
                    round(stdev(ber_lst),7))
            print('--------------------------------------------------------------------')
## run method
# Objectives:
# - define a double match word accuracy test
# - carry out specification on input file
def run(file_name, original_text):
    # list: hold received file transcript
    rcv_text = list()

    ## context manager: open received file for reading
    with open(file_name,'r') as infile:
        for line in infile:
            # break each line into words
            arr = line.split()

            for word in arr:

                # check if word is alphanumeric - no symbols i.e., @, \
                if word.isalnum():
                    # add word to transcription if condition is met
                    rcv_text.append(word)

    # var: total number of bytes in master file transcription
    elements = 0

    # var: total number of bytes in double matched transcription
    match = 0

    # for every element in the master file transcription
    for i in range(0, len(original_text)-1, 1):

        # count bytes of current word
        elements = elements + len(original_text[i])

        # for every element in the received file transcription
        for j in range(0, len(rcv_text)-1, 1):

            # if a match is realised for the word (single match)
            if original_text[i] == rcv_text[j]:

                # if a match is realised for the next word (double match)
                if original_text[i+1] == rcv_text[j+1]:

                    # if double match (phrase identifies), add bytes to match
                    match = match + len(original_text[i])

                    # exit loop
                    break

    # mitigate divide-by-zero error
    if elements > 0:
        ber = (elements - match)/elements
    else:
        # error alert and termination
        print("[ERROR] Original file is empty!")
        ber = 0

    return ber

# run main method
if __name__ == '__main__':
    main()
