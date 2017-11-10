import numpy
import math
import regex
import os
import csv

posunk = "Project1/SentimentDataset/Train/posunk.txt"
negunk = "Project1/SentimentDataset/Train/negunk.txt"
test =  "part6/test.txt"
processedTest = "part6/processed.txt"
resultCsv = "part6/results.txt"
k = .16

# BUILD MODELS ---------------------------------------------------
#keys are first token of bigram, values are ([second words of token], [corresponding number of appearances]) tuples
count_pos = {}
uni_counts_pos = {}
prob_pos = [] 
tokencountPositive = 0
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
        else: 
        	#have not seen this token yet 
        	count_pos[t] = ([tokens[i+1]], [1]) #initialize the tuple 
        if t in uni_counts_pos:
            uni_counts_pos[t] += 1 
        else:
            uni_counts_pos[t] = 1
        tokencountPositive+=1
    tokencountPositive +=1
    if tokens[-1] in uni_counts_pos:
        uni_counts_pos[tokens[-1]] += 1
    else:
        uni_counts_pos[tokens[-1]] = 1 
vocab_size = uni_counts_pos["<unk>"]
bigram_pos = {}
for c in count_pos:
    bigram_pos[c] = ([], []) #tuple is ([list of words], [corresponding P(word | c) values])
    for i,x in enumerate(count_pos[c][1]):
        word = count_pos[c][0][i]
        bigram_pos[c][0].append(word)
        bigram_pos[c][1].append((x+k) / (uni_counts_pos[c]+(k*len(uni_counts_pos)))) #Count(w_n-1 w_n) / count(w_n-1)
    sumP = sum(bigram_pos[c][1])
    for i,x in enumerate(bigram_pos[c][1]):
        bigram_pos[c][1][i] = x / sumP

#keys are first token of bigram, values are ([second words of token], [corresponding number of appearances]) tuples
count_neg = {}
uni_counts_neg = {}
prob_neg = [] 
tokencountNegative = 0
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
        else: 
        	#have not seen this token yet 
        	count_neg[t] = ([tokens[i+1]], [1]) #initialize the tuple 
        if t in uni_counts_neg:
            uni_counts_neg[t] += 1 
        else:
            uni_counts_neg[t] = 1
        tokencountNegative+=1
    tokencountNegative +=1
    if tokens[-1] in uni_counts_neg:
        uni_counts_neg[tokens[-1]] += 1
    else:
        uni_counts_neg[tokens[-1]] = 1 
vocab_size = uni_counts_neg["<unk>"]
bigram_neg = {}
for c in count_neg:
    bigram_neg[c] = ([], []) #tuple is ([list of words], [corresponding P(word | c) values])
    for i,x in enumerate(count_neg[c][1]):
        word = count_neg[c][0][i]
        bigram_neg[c][0].append(word)
        bigram_neg[c][1].append((x+k) / (uni_counts_neg[c]+(k*len(uni_counts_neg)))) #Count(w_n-1 w_n) / count(w_n-1)
    sumP = sum(bigram_neg[c][1])
    for i,x in enumerate(bigram_neg[c][1]):
        bigram_neg[c][1][i] = x / sumP


# GO THROUGH TEST NOW ----------------------------------------------------------------

#Preprocess
f1 = open(processedTest,"w")
for line in open(test):
    line.rstrip()
    tokens = line.split()
    newL = " <s> "
    for t in tokens:
        if t=="''" or t=="'" or  t[0] == "`" or t[0] == '\\':
            continue 
        else:
            newL += t + " "
    newL += " </s>\n"
    newL = newL.lower()
    f1.write(newL)
f1.close()

#results of sentiment assignments to be written to csv 
results = ["Id,Prediction"]
reviewId = 1
for line in open(processedTest):
	line.rstrip()
	tokens = line.split()
	prevToken = "<s>"
	isPositive=0
	isNegative=0
	for t in tokens[1:]:
		#find positive probability
		if prevToken in bigram_pos and t in bigram_pos[prevToken][0]:
			i = bigram_pos[prevToken][0].index(t)
			positiveP = bigram_pos[prevToken][1][i]
		# elif prevToken in bigram_pos and "<unk>" in bigram_pos[prevToken][0]:
		# 	i = bigram_pos[prevToken][0].index("<unk>")
		# 	positiveP = bigram_pos[prevToken][1][i]
		# elif t in uni_counts_pos:
		# 	#we have this word but not this bigram, use smoothed unigram probability
		# 	positiveP = (uni_counts_pos[t]+k) / (tokencountPositive + (k*len(uni_counts_pos)))
		else:
			#set unseen word probabilities to 0
			positiveP = 0
		# find negative probability
		if prevToken in bigram_neg and t in bigram_neg[prevToken][0]:
			i = bigram_neg[prevToken][0].index(t)
			negativeP = bigram_neg[prevToken][1][i]
		# elif prevToken in bigram_neg and "<unk>" in bigram_neg[prevToken][0]:
		# 	i = bigram_neg[prevToken][0].index("<unk>")
		# 	negativeP = bigram_neg[prevToken][1][i]
		# elif t in uni_counts_neg:
		# 	#we have this word but not this bigram, use smoothed unigram probability
		# 	negativeP = (uni_counts_neg[t]+k) / (tokencountNegative + (k*len(uni_counts_neg)))
		else:
			#set unseen word probabilities to 0
			negativeP = 0
		#now add the probabilities to the totals
		isPositive+=positiveP
		isNegative+=negativeP
		prevToken = t 
	if isPositive >= isNegative:
		results.append(str(reviewId)+",0")
	else:
		results.append(str(reviewId)+",1")
	reviewId+=1 
#write results to csv file 
with open(resultCsv, "w") as csvfile:
	for line in results:
		csvfile.write(line + "\n")


