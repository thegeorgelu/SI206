# Using text2 from the nltk book corpa, create your own version of the
# MadLib program.  

# Requirements:
# 1) Only use the first 150 tokens
# 2) Pick 5 parts of speech to prompt for, including nouns
# 3) Replace nouns 15% of the time, everything else 10%

# Deliverables:
# 1) Print the orginal text (150 tokens)
# 1) Print the new text

import nltk
from nltk.book import *
import random

def spaced(word):
	if word in [",", ".", "?", "!", ":"]:
		return word
	else:
		return " " + word

print("START*******")

original_text = ""
for token in text2[11:161]:
	original_text += spaced(token)
print("Original Text -----------------------------------------------------------")
print(original_text)


tokens = nltk.word_tokenize(original_text)
# print("TOKENS")
# print(tokens)
tagged_tokens = nltk.pos_tag(tokens) # gives us a tagged list of tuples
# print("TAGGED TOKENS")
# print(tagged_tokens)
# if debug:
# 	print ("First few tagged tokens are:")
# 	for tup in tagged_tokens[:5]:
# 		print (tup)

tagmap = {"NN":"a noun","RB":"an adverb","VB":"a verb","JJ":"an adjective", "CC":"a coordinating conjunction"}
substitution_probabilities = {"NN":.15,"RB":.1,"VB":.1,"JJ":.1,"CC":.1}

final_words = []


for (word, tag) in tagged_tokens:
	if tag not in substitution_probabilities or random.random() > substitution_probabilities[tag]:
		final_words.append(spaced(word))
	else:
		new_word = input("Please enter %s:\n" % (tagmap[tag]))
		final_words.append(spaced(new_word))

print("New Text ----------------------------------------------------------------")
print ("".join(final_words))


print("\n\nEND*******")





