import numpy
import regex
import os

pos = "Project1/SentimentDataset/Train/pos.txt"
neg = "Project1/SentimentDataset/Train/neg.txt"
pospre = "Project1/SentimentDataset/Train/pospre.txt"
negpre = "Project1/SentimentDataset/Train/negpre.txt"

#preprocessing, add start marks and end marks, change all letters to lower case
f1=open(pospre,"w")
for line in open(pos):
    line = "<s> "+ line + "</s> "
    line = line.lower()
    f1.write(line)
    #print(line)
f1.close()

f2=open(negpre,"w")
for line in open(neg):
    line = "<s> "+ line + "</s> "
    line = line.lower()
    f2.write(line)
    #print(line)
f2.close()





## bigram model for positive
postable = regex.findall(r"\b\w+\s\w+", open(pospre).read(), overlapped=True)
len_postable = len(postable)
print(len_postable)
count_pos = [0 for i in range(len_postable)]
prob_pos = [0 for i in range(len_postable)]
size_postable = float(len_postable)

#count of each bigram combi
for k in range(0 ,len_postable):
    bistr = postable[k]
    with open(pospre) as postmp:
        for line in postmp:
            if bistr in line:
                count_pos[k] += 1

#probability of positive bigram combi
for k in range(0 ,len_postable):
    prob_pos[k] = count_pos[k]/size_postable
    print(k,prob_pos[k],postable[k])



## bigram model for negative
negtable = regex.findall(r"\b\w+\s\w+", open(negpre).read(), overlapped=True)
len_negtable = len(negtable)
print(len_negtable)
count_neg = [0 for i in range(len_negtable)]
prob_neg = [0 for i in range(len_negtable)]
size_negtable = float(len_negtable)

#count of negative bigram combi
for k in range(0 ,len_negtable):
    bistr = negtable[k]
    with open(negpre) as negtmp:
        for line in negtmp:
            if bistr in line:
                count_neg[k] += 1

#probability of negative bigram combi
for k in range(0 ,len_negtable):
    prob_neg[k] = count_neg[k]/size_negtable
    print(k,prob_neg[k],negtable[k])



