############################
# Names: Brady Anderson, Zach Brasseaux, Samantha Santiago
# Date: 4/22/2017
# Objective: Create a cipher puzzle for the Raspberry Pi. Whoever
# is solving has a certain amount of time to solve a puzzle
# to get the correct name of a constellation.
############################
import RPi.GPIO as GPIO
import time

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



class Game():
        def __init__(self):
                self.message = "Hello Everyone"
                #modifies message to criteria
                self.encode_code = cipher.modify_code("A")
                # encypts message
                self.encoded_list = cipher.encode(self.message, self.encode_code)
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

        def get_decrypt(self):
                decode_guess = self.get_pins()
                decode_code = cipher.modify_code(decode_guess)
                decode_string = cipher.decode(self.encoded_list, decode_code)
                print "Decrypted string: ", decode_string
                print decode_guess
                
                return decode_string
                
        

        


# ------------ Encrypt --------------
cipher = Cipher()
game = Game()
solved = False

try:
        while not solved:
                decode_sting = game.get_decrypt()
                solved = game.check_solved(game.message, decode_sting)
                time.sleep(.5)

        GPIO.cleanup()
        
except KeyboardInterrupt:
        GPIO.cleanup()












