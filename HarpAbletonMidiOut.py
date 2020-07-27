import time
import rtmidi
import keyboard
import serial

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

arduino_port = "COM3"

try:
    ser = serial.Serial(arduino_port, 9600)
except:
    print("no arduino in port ", arduino_port)

if available_ports:
    midiout.open_port(1)
else:
    midiout.open_virtual_port("My virtual output")

octive = 5

maxOctive = 8
minOctive = 3
wasChangedOctive = False
wasChangedOctiveDown = False

wasPressed = {'C': False, 'F': False, 'D': False, 'V': False,\
         'B': False, 'N': False, 'J': False, 'M': False, \
        'K': False, ',': False, 'L': False, '.': False}

notesInput = {'C': (0x90, octive * 12, 112), 'F': (0x90, octive * 12 + 1, 112), 'V': (0x90, octive * 12 + 2, 112), 'G': (0x90, octive * 12 + 3, 112),\
         'B': (0x90, octive * 12 + 4, 112), 'N': (0x90, octive * 12 + 5, 112), 'J': (0x90, octive * 12 + 6, 112), 'M': (0x90, octive * 12 + 7, 112), \
        'K': (0x90, octive * 12 + 8, 112), ',': (0x90, octive * 12 + 9, 112), 'L': (0x90, octive * 12 + 10, 112), '.': (0x90, octive * 12 + 11, 112)}

while 1:
    _input = ""
    
    try:
        cc=str(ser.readline())
        # print(cc[2:-5])
        _input = cc.split(',')
    except:
        print('something went wrong while reading Serial port')

    if _input != "":
        for n in notesInput:
            try:
                if (keyboard.is_pressed(n) and not wasPressed[n]) or _input[n] == 1:
                    print('you pressed ', n)
                    midiout.send_message(notesInput[n])
                    wasPressed[n] = True
                if (not keyboard.is_pressed(n)) or _input[n] == -1:
                    midiout.send_message([0x80, notesInput[n][1], notesInput[n][2]])
                    wasPressed[n] = False
            except IndexError:
                print("not enough information to play a note!\n")
            except:
                print('an error has occluded')
        ############################## up octive
        if (keyboard.is_pressed('o') and not wasChangedOctive) or _input[12]:
            wasChangedOctive = True
            octive += 1
            if octive > maxOctive:
                octive =minOctive
            
            print('changing octive to :', octive)
            notesInput = {'C': (0x90, octive * 12, 112), 'F': (0x90, octive * 12 + 1, 112), 'V': (0x90, octive * 12 + 2, 112), 'G': (0x90, octive * 12 + 3, 112),\
             'B': (0x90, octive * 12 + 4, 112), 'N': (0x90, octive * 12 + 5, 112), 'J': (0x90, octive * 12 + 6, 112), 'M': (0x90, octive * 12 + 7, 112), \
            'K': (0x90, octive * 12 + 8, 112), ',': (0x90, octive * 12 + 9, 112), 'L': (0x90, octive * 12 + 10, 112), '.': (0x90, octive * 12 + 11, 112)}
        if not keyboard.is_pressed('o'):
            wasChangedOctive = False
        ################################ down octive
        if keyboard.is_pressed('i') and not wasChangedOctiveDown:
            wasChangedOctiveDown = True
            octive -= 1
            if octive < minOctive:
                octive = maxOctive
            
            print('changing octive to :', octive)
            notesInput = {'C': (0x90, octive * 12, 112), 'F': (0x90, octive * 12 + 1, 112), 'V': (0x90, octive * 12 + 2, 112), 'G': (0x90, octive * 12 + 3, 112),\
             'B': (0x90, octive * 12 + 4, 112), 'N': (0x90, octive * 12 + 5, 112), 'J': (0x90, octive * 12 + 6, 112), 'M': (0x90, octive * 12 + 7, 112), \
            'K': (0x90, octive * 12 + 8, 112), ',': (0x90, octive * 12 + 9, 112), 'L': (0x90, octive * 12 + 10, 112), '.': (0x90, octive * 12 + 11, 112)}
        if not keyboard.is_pressed('i'):
            wasChangedOctiveDown = False
        ##############################stop programme
        if keyboard.is_pressed('esc'):
            break
    else:
        print("not getting any input form port ", arduino_port)
            


