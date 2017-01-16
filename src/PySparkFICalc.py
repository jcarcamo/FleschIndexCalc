# wordcount program

from __future__ import print_function

import sys
import re
from operator import add

from pyspark import SparkContext

def word_mapper(word):
    return (word, 1)

def word_reducer(x,y):
    return x+y

def sentence_mapper(sentence):
    return (len(sentence.split(' ')),1)

def sentence_reducer(x,y):
    return x+y

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: PySparkWordCount <file>", file=sys.stderr)
        exit(-1)
    sc = SparkContext(appName="PySparkWordCount")
    lines = sc.textFile(sys.argv[1], 1)
    word_counts = lines.flatMap(lambda x: x.encode('utf-8').split(' ')) \
                  .map(word_mapper) \
                  .reduceByKey(word_reducer)
    output = word_counts.map(lambda x: x[1]).reduce(lambda x,y: x+y)
    print("WORDS\n %s"%(str(output)))
    
    #for (word, count) in output:
    #    print("%s: %i" %(word, count))
    
    sentence_counts = lines.flatMap(lambda x: re.split('\. |\? ', x.encode('utf-8').replace(u"\u000A"," "))) \
                  .map(sentence_mapper) \
                  .reduceByKey(sentence_reducer)
    
    output = sentence_counts.map(lambda x: x[1]).reduce(lambda x,y: x+y)
    #output = sentence_counts.sum()  #.collect()
    print("SENTENCES\n %s"%(str(output)))
    #for (sentence, count) in output:
    #    print("%s: %i" %(word, count))
    
    sc.stop()

