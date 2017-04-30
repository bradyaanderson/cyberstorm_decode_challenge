import RPi.GPIO as GPIO
import time

letters = {
        3:      "A",
        5:      "B",
        8:      "C",
        7:      "D",
        10:     "E",
        12:     "F",
        11:     "G",
        13:     "H",
        15:     "I",
        16:     "J",
        18:     "K",
        19:     "L",
        22:     "M",
        21:     "N",
        24:     "O",
        23:     "P",
        26:     "Q",
        29:     "R",
        32:     "S",
        31:     "T",
        33:     "U",
        36:     "V",
        35:     "W",
        38:     "X",
        37:     "Y",
        40:     "Z"
}

GPIO.setmode(GPIO.BOARD)
pins = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36,37, 38, 40]
for pin in letters.keys():
        GPIO.setup(pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
        on_list = []
        for pin in letters.keys():
                input_state = GPIO.input(pin)
                if input_state == False:
                        on_list.append(letters[pin])
        print on_list
