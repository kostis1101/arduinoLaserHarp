import time
import rtmidi
import keyboard
import serial

octive = 5


class Note:
    notes = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    the_notes = []

    def __init__(self, note):
        self.note = Note.notes[note]
        global octive
        self.channel = octive * 12 + self.note
        self.was_pressed = False
        Note.the_notes.append(self)

    def start_play(self):
        midiout.send_message([0x90, self.channel, 112])

    def stop_play(self):
        midiout.send_message([0x80, self.channel, 112])

    @staticmethod
    def change_octive():
        global octive
        for n in Note.the_notes:
            n.channel = octive * 12 + n.note


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

maxOctive = 8
minOctive = 3
wasChangedOctive = False
wasChangedOctiveDown = False

notesInput = {'C': Note('C'), 'F': Note('C#'), 'V': Note('D'), 'G': Note('D#'), 'B': Note('E'), 'N': Note('F'),\
              'J': Note('F#'), 'M': Note('G'), 'K': Note('G#'), ',': Note('A'), 'L': Note('A#'), '.': Note('B')}

last_time = 0
times_pressed = 0

while 1:
    _input = []

    try:
        cc = str(ser.readline())
        print(cc[2:-5])
        _input = cc.split(',')
    except:
        print('something went wrong while reading Serial port')
        pass

    if True:
        for n in notesInput:
            try:
                if keyboard.is_pressed(n) and not notesInput[n].was_pressed or _input[n] == 1:
                    print('you pressed ', n)
                    notesInput[n].start_play()
                    notesInput[n].was_pressed = True
                if not keyboard.is_pressed(n): # or _input[n] == -1:
                    notesInput[n].stop_play()
                    notesInput[n].was_pressed = False
            except IndexError:
                print("not enough information to play a note!\n")
            except:
                print('an error has occluded')
        ############################## up octive
        if (keyboard.is_pressed('o') and not wasChangedOctive) or _input[12]:
            wasChangedOctive = True
            times_pressed += 1
            if time.time() - last_time > 1:
                times_pressed = 1
                octive += 1
                if octive > maxOctive:
                    octive = minOctive
            elif times_pressed == 2:
                octive -= 2
                if octive < minOctive:
                    octive = maxOctive
            else:
                octive -= 1
                if octive < minOctive:
                    octive = maxOctive

            print('changing octive to :', octive)
            Note.change_octive()
            last_time = time.time()
        if not keyboard.is_pressed('o'):
            wasChangedOctive = False
        ################################ down octive
        if keyboard.is_pressed('i') and not wasChangedOctiveDown:
            wasChangedOctiveDown = True
            octive -= 1
            if octive < minOctive:
                octive = maxOctive

            print('changing octive to :', octive)
            Note.change_octive()
        if not keyboard.is_pressed('i'):
            wasChangedOctiveDown = False
        ##############################stop programme
        if keyboard.is_pressed('esc'):
            break
    else:
        print("not getting any input form port ", arduino_port)
        pass
