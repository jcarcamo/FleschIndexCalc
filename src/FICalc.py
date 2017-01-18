#!/bin/python
# -*- coding: utf-8 -*-
#
# FICalc.py
# Simple Flesch Index (FI) Calculator
# Break the document down into syllables, words, and sentences. The basic idea
# is that polysyllabic words are more complex than simple words, and sentences
# with a large number of words (requiring a higher cognitive load to keep
# everything in memory) are more complex than short, simple sentences.
#
# Created by: Juan Gonzalo Carcamo
# 01-17-2017
#
###############################################################################
import sys
import re
import time
import operator
import numpy as np
#OSX hack
import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

vowels_list = ['a','e','i','o','u','A','E','I','O','U']

def clean_word(word):
    word = word.replace('.','').replace(',','').replace('“','')
    word = word.replace('‘','').replace('”','').replace('"','')
    word = word.replace('?','').replace('(','').replace(')','')
    word = word.strip()
    return word

def count_syllables(word):
    counter = 0
    is_prev_vowel = False
    for pos, c in enumerate(word):
        if c in vowels_list:
            if not is_prev_vowel:
                is_prev_vowel = True
                counter += 1
        else:
            is_prev_vowel = False
        if pos == len(word)-1:
            if c == 'e' or c == 'E':
                counter-=1
    return counter

def get_fi(syllables_count, words_count, sentences_count):
    return 206.835 - 84.6*(syllables_count/float(words_count)) - 1.015*(words_count/float(sentences_count))

def calculate_fi(file_name):
    f = open(file_name, 'r')
    whole_text = f.read()
    whole_text = whole_text.replace('\r',' ').replace('\n',' ').strip()
    words_list = re.split(' |\-', whole_text)
    senteces_list = re.split('\. |\?|!', whole_text)

    syllables_counter = 0
    words_counter = 0
    sentences_counter = len (senteces_list)

    syllables_stats_dict = {}
    words_stats_dict = {}
    sentences_stats_dict = {}

    for sentence in senteces_list:
        sentence_word_list = sentence.strip().split(' ')
        sentence_word_counter = 0
        for word in sentence_word_list:
            word = clean_word(word)
            if word !=  '' and word != '—':
                sentence_word_counter += 1
        if sentence_word_counter in sentences_stats_dict:
            sentences_stats_dict[sentence_word_counter] += 1
        else:
            sentences_stats_dict.update({sentence_word_counter:1})

    for word in words_list:
        word = clean_word(word)
        if word !=  '' and word != '—':
            words_counter+=1
            if word in  words_stats_dict:
                words_stats_dict[word] += 1
            else:
                words_stats_dict.update({word:1})
            tmp_counter = count_syllables(word)
            if tmp_counter in  syllables_stats_dict:
                syllables_stats_dict[tmp_counter] += 1
            else:
                syllables_stats_dict.update({tmp_counter:1})
            if tmp_counter > 5:
                print "Long word: ", word
            syllables_counter += tmp_counter

    print "SENTENCES: ", sentences_counter
    print "WORDS: ", words_counter
    print "SYLLABLES: ", syllables_counter,"\n\n"

    print "FI: ", get_fi(syllables_counter,words_counter, sentences_counter)

    np_syllables_bins = np.array(syllables_stats_dict.keys(),dtype=int)
    np_syllables_weights = np.array(syllables_stats_dict.values(),dtype=int)

    print "Highest syllable count: ", max(syllables_stats_dict)#len(syllables_stats_dict)-1

    # the histogram of the data
    n, bins, patches = plt.hist(np_syllables_bins, bins=np.arange(min(np_syllables_bins), max(np_syllables_bins) + 1, 1), weights=np_syllables_weights)

    plt.xlabel('Syllables')
    plt.ylabel('Frequency')
    plt.title('Syllables length')
    plt.grid(True)
    plt.show()

    print "Unique words: ", len(words_stats_dict)

    print "Top frequently used word: "
    i = 0
    sorted_by_value = sorted(words_stats_dict, key=words_stats_dict.get, reverse=True)
    for i in range(0,10):
        print i+1, sorted_by_value[i], " appearences: ",words_stats_dict[sorted_by_value[i]]
        i+=1

    np_words_bins = np.arange(1,len(words_stats_dict)+1,1)
    np_words_weights = np.array(words_stats_dict.values(),dtype=float)/words_counter

    n, bins, patches = plt.hist(np_words_bins, bins=np.arange(min(np_words_bins), max(np_words_bins) + 1, 1), weights=np_words_weights)

    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Histogram of words')
    plt.grid(True)
    plt.show()

    np_sentences_bins = np.array(sentences_stats_dict.keys(),dtype=int)
    np_sentences_weights = np.array(sentences_stats_dict.values(),dtype=int)

    print "Highest sentece count: ", max(sentences_stats_dict)

    # the histogram of the data
    n, bins, patches = plt.hist(np_sentences_bins, bins=np.arange(min(np_sentences_bins), max(np_sentences_bins) + 1, 1), weights=np_sentences_weights)
    plt.xlabel('Sentences')
    plt.ylabel('Frequency')
    plt.title('Sentence length')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: FICalc.py <file>"
        exit(-1)
    file_name = sys.argv[1]
    start = time.time()
    calculate_fi(file_name)
    print 'It took', time.time()-start, 'seconds.'
