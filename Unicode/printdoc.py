import sys
import os
import pickle as pkl

# load the unicode dictionaries from the pickle file
dictionaries = pkl.load( open("kannada_unicode.p", "rb"))
myletters = dictionaries[0]
mynumbers = dictionaries[1]
myvowels = dictionaries[2]
myspecials = dictionaries[3]

def decode_word(word):
	myword = ""
	# Split each word into characters with ottaksharas and kagunitas(vowels)
	chars = word.split('C')
	for i in range(1, len(chars)):
		# Keep track of vowels 
		vowelflag = False
		vowel=""
		cons=""
		if('+' in chars[i]):
			""" 
				Vowels exist. Extract vowel and use rest to split into consonant and ottaksharas.
				
				A character with ottaksharas and vowels are always formed in unicode by following method

					main_character + ottakshara_1 + ottakshara_2 +...ottakshara_n + vowel
				
				NOTE: There can be any number of ottaksharas for a main_character but only one vowel

			"""
			vowel = chars[i].split('+')[1]
			vowelflag = True
			cons = chars[i].split('+')[0]
			cons = cons.split('^')
		else:
			cons = chars[i].split('+')[0]
			cons = chars[i].split('^')

		# Start forming character with ottaksharas and vowels to print
		mychar = ""
		for j in range(0,len(cons)):
			# If cons[j] is 53, it is handled in previous iteration. So skip and continue.
			if(int(cons[j])==53):
				continue
			
			mychar += myletters[int(cons[j])]
			      
			""" 
				If ra appears as a main consonant(that is j = 0), we need to preserve it so that it doesnt become a ottakshara.
				This is special case 2 that was discussed above.
			"""
			if(int(cons[j]) == 43 and j==0):
				mychar += myspecials[1]
			"""
				We are at character level, first character is main character, rest are all ottaksharas. 
				So add halant characters in order to form consonant clusters
			"""
			added = False # Bad way of handling this. Change it    
			if(j!=len(cons)-1):
				# Check if next ottakshara to add is 53. If yes, this has to be handled as per special case 1 of ra
				if(j+1!=len(cons)):
					if(int(cons[j+1])==53):
						newchar = myletters[43]                       
						newchar = newchar + myvowels[1] 
						newchar += mychar
						mychar = newchar
						added = True                        
				# Add ottakshara normally
			if(j!=len(cons)-1 and added == False):
				mychar += myvowels[1]

		# Check if vowels exist and add them
		if(vowelflag):
			mychar += myvowels[int(vowel)]
		# print(mychar)
		# Once char is obtained, form words
		myword += mychar
	# Spaces between words
	myword +=" "
	# print(myword)
	return(myword)

"""
	Input form
		L - Seperate lines
		W - Seperate words
		C - Seperate characters
		^ - Seperate ottaksharas in characters
		+ - Seperate vowel
"""

"""
Test Input - 
"LWC36C36^36WC49+9C48C43+5WC46^43+10C42+2LWC36+3C36^36WC49+9C48C43+5WC46+5C40^43C24^42+13C32+3"
"LWC43^36"
"LWC17^43C41"
"LWC17C41^53"
"LWC17C41^53+3" (In previous code, this input wouldnt have worked as 53 was 17th vowel. 
Hence no other vowel could be added as one consonant can have only one vowel. It is fixed now)
"LWC40^43^42" (In previous code, 43 would be considered as second main character even if it had to be an ottakshara to 40. It was fixed)
"""
test_input = "LWC36C36^36WC49+9C48C43+5WC46^43+10C42+2LWC36+3C36^36WC49+9C48C43+5WC46+5C40^43C24^42+13C32+3"


def unicode_to_kn(input):
	lines = input.split('L')
	# print(lines)
	line_count = 0
	word_count = 0
	for i in range(1,len(lines)):
		myline = ""
		print(lines[i])
		line_count += 1
		words = lines[i].split('W')
		for j in range(1, len(words)):
			# print(words[j])
			myword = decode_word(words[j])
			myline = myline + myword
		print(myline)