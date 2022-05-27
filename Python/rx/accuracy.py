## main method
# Objectives:
# - transcribe master file
# - compare test files with master files
def main():
    # list: hold master file transcript
    original_text = list()

    # file array: UART - UART direct connection control environment files
    test_files_control_speed = ['9600_control.txt', '19200_control.txt',
                                '38400_control.txt', '57600_control.txt',
                                '115200_control.txt', '230400_control.txt',
                                '460800_control.txt']

    # file array: vary UART rate to Li-Fi, well-lit environment
    test_files_light_speed = ['light_speed_9600.txt', 'light_speed_19200.txt',
                            'light_speed_38400.txt', 'light_speed_57600.txt',
                            'light_speed_115200.txt', 'light_speed_230400.txt',
                            'light_speed_460800.txt']

    # file array: vary UART rate to Li-Fi, poorly-lit environment
    test_files_dark_speed = ['dark_speed_9600.txt', 'dark_speed_19200.txt',
                            'dark_speed_38400.txt', 'dark_speed_57600.txt',
                            'dark_speed_115200.txt', 'dark_speed_230400.txt',
                            'dark_speed_460800.txt']

    # file array: vary LED - Photodiode distance, well-lit environment
    test_files_light_distance = ['light_distance_10cm.txt', 'light_distance_12cm.txt',
                            'light_distance_15cm.txt', 'light_distance_17.5cm.txt',
                            'light_distance_19.5cm.txt', 'light_distance_23cm.txt',
                            'light_distance_30cm.txt']

    # file array: vary LED - Photodiode distance, poorly-lit environment
    test_files_dark_distance = ['dark_distance_10cm.txt', 'dark_distance_12cm.txt',
                            'dark_distance_15cm.txt', 'dark_distance_17.5cm.txt',
                            'dark_distance_19.5cm.txt', 'dark_distance_23cm.txt',
                            'dark_distance_30cm.txt']

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
        print('------------------------------------------------')

        # run accuracy test on control environment files
        for file in test_files_control_speed:
            run('table1/'+file, original_text)

        # run accuracy test on varied speed, well-lit environment files
        for file in test_files_light_speed:
            run('table2/'+file, original_text)

        # run accuracy test on varied speed, poorly-lit environment files
        for file in test_files_dark_speed:
            run('table3/'+file, original_text)

        # run accuracy test on varied distance, well-lit environment files
        for file in test_files_light_distance:
            run('table4/'+file, original_text)

        # run accuracy test on varied distance, poorly-lit environment files
        for file in test_files_dark_distance:
            run('table5/'+file, original_text)

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

                    # if double match (phrase identifies), add bytes to match pool
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

    # pretty output
    print(file_name, (27 - len(file_name))*' ',"|\t", round(ber,7))
    print('------------------------------------------------')

# run main method
if __name__ == '__main__':
    main()
