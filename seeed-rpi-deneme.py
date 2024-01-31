#%%
#!/usr/bin/env python
import serial
import time
from Radar import RADAR
import RPi.GPIO as GPIO
#%%

MESSAGE_HEAD = "55"
data = ['00']*34
i = 0
Msg = 0
Situation_action = 0
Fall_action = 0


# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(15, GPIO.IN)
# GPIO.setup(16, GPIO.OUT)


def concatenate_hex_bytes(data):
    # Extract bytes 1-43 from data
    bytes = data[0:43]

    # Convert each byte to hexadecimal string
    hex_strings = [format(b, '02x') for b in bytes]

    # Concatenate hex strings
    hex_string = ''.join(hex_strings)
    return hex_string


def hex_to_int(value_str):
    return int(value_str, 16)


# Set up serial communication on GPIO pins
ser = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS
)

# Wait for the serial connection to be established
time.sleep(2)

def data_length(data):
    data = hex_to_int(data)
    return data

    
# Define function to handle body sign judgment
def Bodysign_judgment(ad1, ad2, ad3, ad4, ad5):
    s = RADAR.Bodysign_val(ad1, ad2, ad3, ad4, ad5)
    # print(s)
    if s > 1.5 and s < 35:
        print("SOMEBODY STOP")
    elif s < 1.5:
        print("NOBODY")
    elif s > 35:
        print("SOMEBODY MOVE")

print("............... Fall Detection Module is activated ...............")
# Read data from serial port and process it
while True:
    Msg = concatenate_hex_bytes(ser.read())
    # print(Msg)
    if Msg == MESSAGE_HEAD:
        data[0] = Msg
        Msg = concatenate_hex_bytes(ser.read())
        data[1] = Msg
        for i in range(data_length(Msg)):
            data[i+2] = Msg
            Msg = concatenate_hex_bytes(ser.read())

        if Msg == MESSAGE_HEAD:
            # Situation_action = RADAR.Situation_judgment(data[5], data[6], data[7], data[8], data[9]) # situation function
            # if Situation_action == 1:
            #     print("radar said nobody")
            # elif Situation_action == 2:
            #     print("radar said somebody move")
            # elif Situation_action == 3:
            #     print("radar said somebody stop")
            # elif Situation_action == 4:
            #     print("radar said no move")
            # elif Situation_action == 5:
            #     print("radar said somebody close")
            # elif Situation_action == 6:
            #     print("radar said somebody away")


            Fall_action = RADAR.Fall_judgment(data[4], data[5], data[6], data[7]) # fall function
            if Fall_action == 1:
                # IoT Fall Alert
                # GPIO.output(16, GPIO.HIGH)
                print("SUSPECTED FALL")
            elif Fall_action == 2:
                print("REAL FALL")
            elif Fall_action == 3:
                # GPIO.output(16, GPIO.LOW)
                print("NO FALL")
            elif Fall_action == 4:
                print("NO WARNING")
            elif Fall_action == 5:
                print("FIRST WARNING")
            elif Fall_action == 6:
                print("SECOND WARNING")
            elif Fall_action == 7:
                print("THIRD WARNING")
            elif Fall_action == 8:
                print("FORTH WARNING")

        time.sleep(0.002)
        
        
        








# %%
