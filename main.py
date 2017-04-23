############################
# Names: Brady Anderson, Zach Brasseaux, Samantha Santiago
# Date: 4/22/2017
# Objective: Create a cipher puzzle for the Raspberry Pi. Whoever
# is solving has a certain amount of time to solve a puzzle
# to get the correct name of a constellation.
############################

# modifies string value to be only unique characters and all uppercase
def modify_code(string):
	if type(string) is str:
		string = list(string)
	# activity will only work with upper letters, makes all characters upper
	string = [char.upper() for char in string]
	return "".join(list(set(string)))

# takes a list of characters or strings and returns a list of integers representing characters
def str_to_int(string):
	# checks if string. if not string, assumes list of characters
	if type(string) is str:
		string = list(string)
	return [ord(char) for char in string]


# takes a list of integers and converts to string of readable characters
def int_to_string(int_list):
	return "".join([chr(i) if (i < 128 and i > 31) else chr(32 + i % 96) for i in int_list])

def cipher(char_int_list, code_int_list, crypt):
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
def encode(string, code):
	char_int_list = str_to_int(string)
	code_int_list = str_to_int(code)
	char_int_list = cipher(char_int_list, code_int_list, "encrypt")
	return char_int_list

# decypts string
def decode(encoded_list, code):
	code_int_list = str_to_int(code)

	encoded_list = cipher(encoded_list, code_int_list, "decrypt")
	return int_to_string(encoded_list)


# ------------ Encypt --------------
message = "Hello Everybody"
encode_code = modify_code('Potatoes')

encoded_list = encode(message, encode_code)
print "Encrypted string:" ,int_to_string(encoded_list)


# ------------ Decode --------------
decode_guess = ['P','o', 't', 'A','E','S']
decode_code = modify_code(decode_guess)
decode_string = decode(encoded_list, decode_code)

print "Decypted string: ", decode_string