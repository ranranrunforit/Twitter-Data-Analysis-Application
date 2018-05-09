# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:17:20 2018

@author: chaoran
"""

import nltk
from nltk.corpus import brown
from tabulate import tabulate
from collections import defaultdict

tags = brown.tagged_words()
cfd = nltk.ConditionalFreqDist(tags)

num_tags = []
for condition in cfd.conditions():
    num_tags.append((condition, len(cfd[condition])))


tags_by_num = []

for i in range(11):
    this_num = 0
    for (word, num) in num_tags:
        if num == i:
            this_num += 1
    if i > 0:
        tags_by_num.append((i, this_num))

print("Table for part1")
# prints a table of the integers 1-10 and the numbers of distinct words in the corpus that have those numbers of distinct tags
print(tabulate(tags_by_num, headers=["the integers", "the number of distinct words in the corpus having distinct tags"]))



num_tags = list(reversed(sorted(num_tags, key=lambda x: x[1])))
# "that" is the word with the greatest number of distinct tags
#print(num_tags[0][0])
#output that

wordX = num_tags[0][0]
distinct_tags = [tag for tag in cfd[wordX]]

tagged_sents = brown.tagged_sents()

print("Sentences from the corpus containing the word, one for each possible tag.")
# go through each sentence in the corpus. 
# go through each tag in the sentence

for sent in tagged_sents:
    for (word, tag) in sent:
        for distinct_tag in distinct_tags:
            if distinct_tag == tag and word == wordX:
                print(sent)
                distinct_tags.remove(distinct_tag)
                print("*******************************************************")             
                break
    
print("Table for part3 (result1):")
#part 3 way 1
#######################################################################
tagfd = nltk.FreqDist(t for (w,t) in tags)
#print(len(tagfd))
#print(tagfd.most_common(10))
tagfd = tagfd.most_common(10)

new = []
for x in tagfd:
    #print (x[0], x[1])
    new.append(x[1])
    
new2 =[1,2,3,4,5,6,7,8,9,10]

tags_2 = zip(new2,new)

# prints a table of the integers 1-10 and the numbers of distinct words in the corpus that have those numbers of distinct tags

print(tabulate(tags_2, headers=["the integers ", "the number of words of each tag"]))



print("Table for part3 (result2):")   
#part 3 way 2
#######################################################################   

word_tag = defaultdict(set)
for w,t  in  tags:
    word_tag[t].add(w)
    
#m = max(len(word_tag[t]) for t in word_tag)
#print (m)

n_w = []
for t in word_tag:
    n_w.append((t, len(word_tag[t])))

#print(len(n_w))
#print (n_w)
n_t = list(reversed(sorted(n_w, key=lambda x: x[1])))
#print (n_t)
new = []
for x in n_t[:10]:
    #print (x[0], x[1])
    new.append(x[1])
    
new2 =[1,2,3,4,5,6,7,8,9,10]

tags_2 = zip(new2,new)
print(tabulate(tags_2, headers=["the integers ", "the number of words of each tag"]))