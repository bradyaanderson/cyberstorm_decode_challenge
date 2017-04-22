############################
# Names: Brady Anderson, Zach Brasseaux, Samantha Santiago
# Date: 4/22/2017
# Objective: Create a cipher puzzle for the Raspberry Pi. Whoever
# is solving has a certain amount of time to solve a puzzle
# to get the correct name of a constellation.
############################
from Tkinter import *
# import RPi.GPIO as GPIO
import codecs

# encodes a string given a certain value
def encode(string, code):
	pass

# decodes a string given a certain value
def decode(string, code):
	pass

# the answer will be equal to some string value
def get_answer():
	return "some string", "some code value"


# main
solved = False
answer, code = get_answer()
code = "some random value"

# encodes the message as some value
encode_value = encode(answer, code)

# continues until solved
while not solved:

	guess_value = "something"

	# when correct code is input into decode, correct value will be returned
	decode_value = decode(guess_value, code)

	if decode_value == encode_value:
		not_solved = True