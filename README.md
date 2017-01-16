# Flesch Index (FI) Calculator
Break the document down into syllables, words, and sentences. The basic idea is
that polysyllabic words are more complex than simple words, and sentences with 
a large number of words (requiring a higher cognitive load to keep everything 
in memory) are more complex than short, simple sentences.

These two intuitions are captured in the succinct equation below:

```
FI = 206.835 - 84.6*(numSyllables/numWords) - 1.015*(numWords/numSentences)
```
