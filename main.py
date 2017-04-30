############################
# Names: Brady Anderson, Zach Brasseaux, Samantha Santiago
# Date: 4/22/2017
# Objective: Create a cipher puzzle for the Raspberry Pi. Whoever
# is solving has a certain amount of time to solve a puzzle
# to get the correct name of a constellation.
############################
import RPi.GPIO as GPIO
from Tkinter import *
from time import time, sleep
from datetime import timedelta


# holds all functions related to cipher
class Cipher():

    # modifies string value to be only unique characters and all uppercase
    def modify_code(self, string):
            if type(string) is str:
                    string = list(string)
            # activity will only work with upper letters, makes all characters upper
            string = [char.upper() for char in string]
            return "".join(list(set(string)))

    # takes a list of characters or strings and returns a list of integers representing characters
    def str_to_int(self, string):
            # checks if string. if not string, assumes list of characters
            if type(string) is str:
                    string = list(string)
            return [ord(char) for char in string]


    # takes a list of integers and converts to string of readable characters
    def int_to_string(self, int_list):
            return "".join([chr(i) if (i < 128 and i > 31) else chr(32 + i % 96) for i in int_list])

    def cipher(self, char_int_list, code_int_list, crypt):
            # integers added, removed, or changed, as well as a change of index, will affect how message is ciphered
            cipher_values = [1, 2, 3, 4, 5, 6, 8]

            # changes modifer depending on crypt
            if crypt == "encrypt":
                    modifier = 1
            elif crypt== "decrypt":
                    modifier = -1
            else:
                    raise ValueError("valid arguement for crypt are 'encrypt' or 'decrypt'")

            # ciphers based on code and cipher values
            for i in range(len(code_int_list)):
                    for j in range(len(cipher_values)):
                            char_int_list = [char_int_list[k]  + code_int_list[i] * modifier  if (j + k) % cipher_values[j] == 0 else char_int_list[k] for k in range(len(char_int_list))]

            return char_int_list


    # encrypts string
    def encode(self, string, code):
            char_int_list = self.str_to_int(string)
            code_int_list = self.str_to_int(code)
            char_int_list = self.cipher(char_int_list, code_int_list, "encrypt")
            return char_int_list

    # decypts string
    def decode(self, encoded_list, code):
            code_int_list = self.str_to_int(code)

            encoded_list = self.cipher(encoded_list, code_int_list, "decrypt")
            return self.int_to_string(encoded_list)


# creates a timer object
class Timer(object):
    def __init__(self, total_time):
        self.total_time = total_time
        self.start_time = time()

    def get_time_left(self):
        current_time_left = self.total_time - time() + self.start_time
        if current_time_left > 0:
            return str(timedelta(seconds=current_time_left+1))[3:7]
        return '0:00'


# creates main challenge object
class Challenge(Cipher):
    def __init__(self):
        # game variables
        self.game_over = False
        self.game_win = False
        self.message = "123456789012345"
        #modifies message to criteria
        self.encode_code = self.modify_code("A")
        # encypts message
        self.encoded_list = self.encode(self.message, self.encode_code)
        # gpio with corresponding letter
        self.letters = {
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

        self.pins = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36,37, 38, 40]
        # set up GPIO
        self.setup_gpio()

    # sets up GPIO inputs for game
    def setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        for pin in self.letters.keys():
            GPIO.setup(self.pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # returns a list of letters for each grounded pin
    def get_pins(self):
        on_pins = []
        for pin in self.letters.keys():
            input_state = GPIO.input(pin)
            if input_state == False:
                on_pins.append(self.letters[pin])
        return on_pins

    # return true or false depending on if user has solved message
    def check_solved(self, message, decode_string):
        if message == decode_string:
            return True
        return False

    # returns decrypted message based on what pins are high / low
    def get_decrypt(self):
        decode_guess = self.get_pins()
        decode_code = self.modify_code(decode_guess)
        decode_string = self.decode(self.encoded_list, decode_code)
        return decode_string


# creates gui
class App(Challenge, Timer):
    def __init__(self):
        # set up challenge and tieme
        Challenge.__init__(self)
        Timer.__init__(self, 300)
        
        # set up gui components
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.root = Tk()
        self.root.title("Constellation Crack")
        self.root.configure(bg="black")
        self.root.geometry('{}x{}'.format(self.WIDTH, self.HEIGHT))
        self.set_up_gui()

        # update gui components
        self.update_timer()
        self.update_challenge()

        # Tkinter mainloop
        self.root.mainloop()

    # updates the gui timer
    def update_timer(self):
        self.timer.configure(text=self.get_time_left())
        self.root.after(100, self.update_timer)

    # updates all components of gui related to challenge
    def update_challenge(self):
        decode_string = self.get_decrypt()
        self.code.configure(text=decode_string)
        self.root.after(10, self.update_challenge)


    # sets up GUI for application
    def set_up_gui(self):
        self.widget_w = int(self.WIDTH/80)
        self.widget_h = int(self.HEIGHT/130)

        self.set_up_code_box(1, 0)
        self.set_up_timer_box(0, 0)
        self.set_up_image_box(0, 1)
        self.set_up_hints_box(1, 1)

    # set up code box
    def set_up_code_box(self, r, c):
        self.code = Label(self.root, text="DF%$JD!WEK]", bg="black", fg="white", width=self.widget_w, height=self.widget_h, font=("Courier", 50))
        self.code.grid(row=r, column=c)

    # set up timer box
    def set_up_timer_box(self, r, c):
        self.timer = Label(self.root, text="This is where the timer will be", bg="black", fg="white", width=self.widget_w, height=self.widget_h, font=("Courier", 50))
        self.timer.grid(row=r, column=c)

    # set up image box
    def set_up_image_box(self, r, c):
        photo = PhotoImage(file="test.gif")
        self.image = Label(self.root, image=photo, width=640, height=360, bg="black")
        self.image.image = photo
        self.image.grid(row=r, column=c)

    # set up hints box
    def set_up_hints_box(self, r, c):
        self.hints = Label(self.root, text="This is where the hints will be\n I think", bg="black", fg="white", width=int(self.widget_w * (2.5)), height=int(self.widget_h * (2.6)), font=("Courier", 20))
        self.hints.grid(row=r, column=c)


# ----- MAIN -----

try:
    app = App()
except KeyboardInterrupt:
        GPIO.cleanup()
        
