#!/bin/python
import re

vowels_list = ['a','e','i','o','u','A','E','I','O','U']

def count_syllables(word):
    counter = 0
    for pos, c in enumerate(word):
        if c in vowels_list:
            counter += 1
    return counter

def get_fi(syllables_count, words_count, sentences_count):
    return 206.835 - 84.6*(syllables_count/words_count) - 1.015*(words_count/sentences_count)

f = open('../data/NYTimes.txt', 'r')
whole_text = f.read()#.decode('string_escape')
#whole_text = ' '.join(unicode(whole_text, 'utf-8').splitlines())
whole_text = whole_text.replace('\r',' ').replace('\n',' ').strip()
words_list = whole_text.split(' ')
senteces_list = re.split('\. |\?|!', whole_text)

i=1
for sentence in senteces_list:
    if i < 10:
        print i,sentence.strip()
    i+=1

syllables_counter = 0

for word in words_list:
    syllables_counter += count_syllables(word)

print "WORDS: ", len(words_list)
print "SENTENCES: ", len(senteces_list)
print "SYLLABLES: ", syllables_counter,"\n\n"

print "FI: ", get_fi(syllables_counter,len(words_list), len(senteces_list))
