# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 15:04:16 2018

@author: chaoran
"""

#Find hashtags script. This is a simple script to read csv and find hashtags

import csv, nltk
from nltk.tokenize import word_tokenize
import operator
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

result = []
s = []
handles = []
hdict = {}
   
corpus = []
with open ('elonmusk_tweets.csv', 'rb') as infile:
    reader = csv.reader(infile,quotechar='"')
    for row in reader:
        #print "row"
        #print row
        tokens = word_tokenize(row[2])
        #print "tokens"
        #print tokens
        
        corpus.append(row[2])

        handles = [i for i in row[2].split() if i.startswith("@")]
        #print handles

        for word in tokens:
            #print word
            if word not in s: 
                s.append(word)

        if len(handles) != 0:
            for h in handles:
                key = h
                if key not in result:
                    count = 1
                    result.append(key)
                    hdict[key] = count
                else:
                    count += 1
                    hdict[key] = count

hdict = sorted(hdict.items(), key=operator.itemgetter(1), reverse=True)
#hdict = sorted(hdict.items(), key=lambda x: x[1])

#print s
#for x in s:
#    print x
#for k in hdict:
#    print k

print "The top handles used in the tweets: "
print hdict[0][0]


#print len(corpus)

#vectorize the text 
vectorizer = TfidfVectorizer(lowercase=True, stop_words="english", norm=None, use_idf=True, smooth_idf=False,sublinear_tf=False, decode_error="ignore")
vectors = vectorizer.fit_transform(corpus)
names = vectorizer.get_feature_names()
#new = zip(names,vectors.todense())

#print vectors
#print names

#max_iter = 100 is better than 1000
true_k = 2
#use kmeans to cluster documents
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1)
model.fit(vectors)
predict = model.fit_predict(vectors)
#print len(predict)

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()


clusters = {}

for i in range(true_k):
    clist = []
    for ind in np.where(predict==i)[0]:
        #print ind
        clist.append(corpus[ind])    
    clusters[i] = clist

#c = Counter()

for i in range(true_k):
    print "\n"
    print "\nCluster %d:" % i,
    c = Counter()
    for tw in clusters[i]:
        for word in tw.split():
            c[word] +=1

    #for k,v in c.items():
    handcount = []
    hashcount = []
    for k,v in c.most_common(2000):
        if k.startswith("@") :
            handcount.append(k)
            #print "\nTop handle: %s" % k
        if k.startswith("#") :
            hashcount.append(k)
            #print "\nTop hashtag: %s" % k
    
    if len(handcount) == 0:
        print "\nTop handles: \nNone."
    else:
        print "\nTop handles: "
        for x in handcount[:10]:
            print x

    if len(hashcount) == 0:
        print "\nTop hashtags: \nNone."
    else:
        print "\nTop hashtags: "
        for x in hashcount[:10]:
            print x
    
    #print "\nTop word: %s " % c.most_common(1)

    print "\nTop words: "
    for ind in order_centroids[i, :10]:
        #print ind
        print terms[ind]

