import numpy
import math
import regex
import os

pos = "Project1/SentimentDataset/Train/pos.txt"
neg = "Project1/SentimentDataset/Train/neg.txt"
pospre = "Project1/SentimentDataset/Train/pospre.txt"
negpre = "Project1/SentimentDataset/Train/negpre.txt"
posunk = "Project1/SentimentDataset/Train/posunk.txt"
negunk = "Project1/SentimentDataset/Train/negunk.txt"
posselected = "Project1/SentimentDataset/Dev/pos.txt"
negselected = "Project1/SentimentDataset/Dev/neg.txt"
posselected1 = "Project1/SentimentDataset/Train/posselected.txt"
negselected1 = "Project1/SentimentDataset/Train/negselected.txt"

#preprocessing, add start marks and end marks, change all letters to lower case
f1 = open(pospre,"w")
for line in open(pos):
    line.rstrip()
    tokens = line.split()
    newL = " <s> "
    for t in tokens:
        if "'" in t or t[0] == "`" or t[0] == '\\':
            continue
        else:
            newL += t + " "
    newL += " </s>\n"
    newL = newL.lower()
    f1.write(newL)
f1.close()

f2 = open(negpre,"w")
for line in open(neg):
    line.rstrip()
    tokens = line.split()
    newL = " <s> "
    for t in tokens:
        if "'" in t or t[0] == "`" or t[0] == '\\':
            continue
        else:
            newL += t + " "
    newL += " </s>\n"
    newL = newL.lower()
    f2.write(newL)
f2.close()

##work with unknown words
#replace the first occurrence of every word type in the training data by <unk>
tag_pos = []
f1u = open(posunk,"w")
for line in open(pos):
    line.rstrip()
    tokens = line.split()
    newL = " <s> "
    for t in tokens:
        if "'" in t or t[0] == "`" or t[0] == '\\':
            continue
        else:
            if t in tag_pos:
                newL += t + " "
            else:
                tag_pos.append(t)
                t="<unk>"
                newL += t + " "
    newL += " </s>\n"
    newL = newL.lower()
    f1u.write(newL)
f1u.close()

tag_neg = []
f2u = open(negunk,"w")
for line in open(neg):
    line.rstrip()
    tokens = line.split()
    newL = " <s> "
    for t in tokens:
        if "'" in t or t[0] == "`" or t[0] == '\\':
            continue
        else:
            if t in tag_neg:
                newL += t + " "
            else:
                tag_neg.append(t)
                t="<unk>"
                newL += t + " "
    newL += " </s>\n"
    newL = newL.lower()
    f2u.write(newL)
f2u.close()

## new bigram table with smoothing-----------------------------------------------------------------------------------------------
#keys are first token of bigram, values are ([second words of token], [corresponding number of appearances]) tuples
count_pos = {}
uni_counts_pos = {}
prob_pos = []
postype = []
Vpos = 0
for line in open(posunk):
    line.rstrip()
    tokens = line.split()
    for t in tokens:
        if t in postype:
            continue
        else:
            postype.append(t)
            Vpos += 1
for line in open(posunk):
    tokens = line.split()
    line.rstrip()
    for i,t in enumerate(tokens[:-1]):
        if t in count_pos:
            if tokens[i+1] in count_pos[t][0]: #we have already recorded this specific bigram
                index = count_pos[t][0].index(tokens[i+1])
                count_pos[t][1][index] += 1 #increment count
            else:  #we have not encountered this bigram yet
                count_pos[t][0].append(tokens[i+1]) #add this bigram
                count_pos[t][1].append(1) #start with 1 appearance
        else: #have not seen this token yet
            count_pos[t] = ([tokens[i+1]], [1]) #initialize the tuple
        if t in uni_counts_pos:
            uni_counts_pos[t] += 1
        else:
            uni_counts_pos[t] = 1
    if tokens[-1] in uni_counts_pos:
        uni_counts_pos[tokens[-1]] += 1
    else:
        uni_counts_pos[tokens[-1]] = 1
bigram_pos = {}
posline = []
plsize = 0
for line in open(posselected):
    line.rstrip()
    tokens = line.split()
    for t in tokens:
        if t in count_pos:
            posline.append(t)
        else:
            posline.append("<unk>")
        plsize += 1
maxpos = 0
posk = 0
for m in range(1,101):
    k = m/100
    for c in count_pos:
        bigram_pos[c] = ([], []) #tuple is ([list of words], [corresponding P(word | c) values])
        for i,x in enumerate(count_pos[c][1]):
            word = count_pos[c][0][i]
            bigram_pos[c][0].append(word)
            bigram_pos[c][1].append( ( x + k ) / ( uni_counts_pos[word] + k * Vpos ) ) #Count(w_n-1 w_n) + k / count(w_n-1) + k * V
        sumP = sum(bigram_pos[c][1])
        for i,x in enumerate(bigram_pos[c][1]):
            bigram_pos[c][1][i] = x / sumP
    p = 0
    for j in range(0,plsize-1):
        tag = 0
        for i,x in enumerate(bigram_pos[posline[j]][0]):
            if bigram_pos[posline[j]][0][i]==posline[j+1]:
                p += math.log(bigram_pos[posline[j]][1][i])  #Find bigrams
                tag = 1
        if tag == 0:
            p += math.log( k / (uni_counts_pos[posline[j]] + k * Vpos))  #Find unseen bigrams
    if k==0.01:
        maxpos = p
        posk = k
    else:
        if p>maxpos:
            maxpos = p
            posk = k
    #print(p)
print("k for pos-smoothing: " ,posk)

count_neg = {}
uni_counts_neg = {}
prob_neg = []
negtype = []
Vneg = 0
for line in open(negunk):
    line.rstrip()
    tokens = line.split()
    for t in tokens:
        if t in negtype:
            continue
        else:
            negtype.append(t)
            Vneg += 1
for line in open(negunk):
    tokens = line.split()
    line.rstrip()
    for i,t in enumerate(tokens[:-1]):
        if t in count_neg:
            if tokens[i+1] in count_neg[t][0]: #we have already recorded this specific bigram
                index = count_neg[t][0].index(tokens[i+1])
                count_neg[t][1][index] += 1 #increment count
            else:  #we have not encountered this bigram yet
                count_neg[t][0].append(tokens[i+1]) #add this bigram
                count_neg[t][1].append(1) #start with 1 appearance
        else: #have not seen this token yet
            count_neg[t] = ([tokens[i+1]], [1]) #initialize the tuple
        if t in uni_counts_neg:
            uni_counts_neg[t] += 1
        else:
            uni_counts_neg[t] = 1
    if tokens[-1] in uni_counts_neg:
        uni_counts_neg[tokens[-1]] += 1
    else:
        uni_counts_neg[tokens[-1]] = 1
bigram_neg = {}
negline = []
nlsize = 0
for line in open(negselected):
    line.rstrip()
    tokens = line.split()
    for t in tokens:
        if t in count_neg:
            negline.append(t)
        else:
            negline.append("<unk>")
        nlsize += 1
maxneg = 0
negk = 0
for m in range(1,101):
    k = m/100
    for c in count_neg:
        bigram_neg[c] = ([], []) #tuple is ([list of words], [corresponding P(word | c) values])
        for i,x in enumerate(count_neg[c][1]):
            word = count_neg[c][0][i]
            bigram_neg[c][0].append(word)
            bigram_neg[c][1].append( ( x + k ) / ( uni_counts_neg[word] + k * Vneg ) ) #Count(w_n-1 w_n) + k / count(w_n-1) + k * V
        sumP = sum(bigram_neg[c][1])
        for i,x in enumerate(bigram_neg[c][1]):
            bigram_neg[c][1][i] = x / sumP
    p = 0
    for j in range(0, nlsize-1):
        tag = 0
        for i, x in enumerate(bigram_neg[negline[j]][0]):
            if bigram_neg[negline[j]][0][i] == negline[j + 1]:
                p += math.log(bigram_neg[negline[j]][1][i])  #Find bigrams
                tag = 1
        if tag == 0:
            p += math.log( k / ( uni_counts_neg[negline[j]] + k * Vneg ) )  #Find unseen bigrams
    if k == 0.01:
        maxneg = p
        negk = k
    else:
        if p > maxneg:
            maxneg = p
            negk = k
    #print(p)
print("k for neg-smoothing: " ,negk)
# end new bigram table with smoothing--------------------------------------------------------------------------------
# using posselected and negselected as held-out data ------  k for pos-smoothing is 1.0    k for neg-smoothing is 1.0
# using posselected1 and negselected1 as held-out data ----  k for pos-smoothing is 0.72   k for neg-smoothing is 1.0