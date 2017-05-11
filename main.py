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
from random import randint

GPIO.setwarnings(False)
DEBUG = 2

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
            return str(timedelta(seconds=current_time_left+1))[3:7], current_time_left
        return '0:00', 0


# creates main challenge object
class Challenge(Cipher):
    def __init__(self):
        # game variables
        self.game_over = False
        self.game_win = False
        self.message = "You Win!!!"
            

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

        self.constellations = {
                               'Scorpius':  [
                                                'Location: southwest', 
                                                '8 letters, with 1 repeating',
                                                'The name Malfoy chose \nfor his kid',
                                                'Scorpion'
                                            ],

                               'Draco':     [   
                                                'Fiery personality.',
                                                '5 letters, no repeats',
                                                'Scales, not feathers',
                                                'Dragon'
                                            ],

                               'Hydra':     [
                                                'Lives in the sea',
                                                '5 letters, no repeat',
                                                'Can’t just cut it off.\nLose one, gain two more.',
                                                'Hail! Water Snake'
                                            ],

                               'Pisces':    [   
                                                'Water Dwellers',
                                                '6 letters, with 1 repeating',
                                                'Life goes swimmingly for them',
                                                'Fish'
                                            ],

                               'Aries':     [
                                                'One to pick a fight',
                                                '5 letters, no repeat',
                                                'Warmonger of the gods',
                                                'Ram'
                                            ],

                               'Crater':    [
                                                'It’s the pits for this one',
                                                '6 letters, with 1 repeating',
                                                'The impact of a meteorite \ncan make one',
                                                'Cup'
                                            ],

                               'Taurus':    [
                                                'Spaniards have a long history \nwith this one',
                                                '6 letters, with 1 repeating',
                                                'Good luck grabbing it by \nthe horns',
                                                'Bull'
                                            ],

                               'Lyra':      [
                                                'Don’t get caught in \nthe strings',
                                                '4 letters, no repeats',
                                                'Classic music choice \nof the Greeks. It’s better \nto strum',
                                                'Lyre'
                                            ]
                               }

        # randomly choosey a constellation.  This will be the secret code for the game
        self.chosen_constellation = self.constellations.keys()[randint(0,len(self.constellations) - 1)]

        if DEBUG >= 1:
            print self.chosen_constellation

        # modifies code to criteria, this is the secret code that needs to be cracked
        self.encode_code = self.modify_code(self.chosen_constellation)

        # if level 2 debug, secret code is set to A
        if DEBUG >= 2:
            self.encode_code = self.modify_code("A")

            # encypts message
        self.encoded_list = self.encode(self.message, self.encode_code)

        # set up GPIO
        self.setup_gpio()

    # sets up GPIO inputs for game
    def setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        for pin in self.letters.keys():
            GPIO.setup(self.letters.keys(), GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
        Timer.__init__(self, 10)
        
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

        # clean GPIO after window closes
        GPIO.cleanup()

    # updates the gui timer
    def update_timer(self):
        time_left_string , self.time_left = self.get_time_left()
        self.timer.configure(text=time_left_string)
        
        # if game is not over or won, keep updating gui   
        if not self.game_over and not self.game_win:
            self.root.after(100, self.update_timer)

    # updates all components of gui related to challenge
    def update_challenge(self):
        decode_string = self.get_decrypt()
        self.code.configure(text=decode_string)
        hint_text = self.show_hints(self.time_left)

        self.hints.configure(text=hint_text)

        # if message is decoded correctly set game_win to true
        if decode_string == self.message:
            self.game_win = True

        # if time left is 0, set game_over to true
        if self.time_left == 0:
            self.hints.configure(text="YOU LOSE")
            self.game_over = True

        # if game is not over or won, keep updating gui    
        if not self.game_over and not self.game_win:
            self.root.after(10, self.update_challenge)

    def show_hints(self, time_left):
        # percent of total time left
        p_time_left = time_left / float(self.total_time)

        # a new hint will show every time 10% of time is up
        if p_time_left < .1:
            return self.constellations[self.chosen_constellation][3] # shows 4th hint (english name)
        elif p_time_left < .2:
            return "Hurry there's not much \ntime left!" # tells to hurry
        elif p_time_left < .3:
            photo = PhotoImage(file="images/" + self.chosen_constellation + ".gif")
            self.image.configure(image=photo)
            self.image.image = photo
            return 'No hint here' # image will change here
        elif p_time_left < .4:
            return self.constellations[self.chosen_constellation][2] # shows 3rd hint relating to constellation
        elif p_time_left < .5:
            return "Don't worry about repeating letters" # informs that repeat letters are not significant
        elif p_time_left < .6:
            return self.constellations[self.chosen_constellation][1] # shows 2nd hint (work length / repeat)
        elif p_time_left < .7:
            return 'Really nice weather we are having \ntoday' # joke
        elif p_time_left < .8:
            return self.constellations[self.chosen_constellation][0] # shows 1st hint
        elif p_time_left < .9:
            return 'There are 26 letters in\nthe alphabet' # show significance of GPIO to letters


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
        photo = PhotoImage(file="images/test.gif")
        self.image = Label(self.root, image=photo, width=640, height=360, bg="black")
        self.image.image = photo
        self.image.grid(row=r, column=c)

    # set up hints box
    def set_up_hints_box(self, r, c):
        self.hints = Label(self.root, text="This is where the hints will be\n I think...", bg="black", fg="white", width=int(self.widget_w * (2.5)), height=int(self.widget_h * (2.6)), font=("Courier", 20))
        self.hints.grid(row=r, column=c)


# ----- MAIN -----
app = App()
        