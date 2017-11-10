import numpy
import math
import regex
import os

posunk = "Project1/SentimentDataset/Train/posunk.txt"
negunk = "Project1/SentimentDataset/Train/negunk.txt"
posselected = "Project1/SentimentDataset/Dev/bigrampositive.txt"
negselected = "Project1/SentimentDataset/Dev/bigramnegative.txt"
k = .16



#keys are first token of bigram, values are ([second words of token], [corresponding number of appearances]) tuples
count_pos = {}
uni_counts_pos = {}
prob_pos = [] 
tokencount = 0
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
        tokencount+=1
    tokencount +=1
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

totalprob = 0
for key in bigram_pos:
	for p in bigram_pos[key][1]:
		totalprob+=p
#PEREPLXITY]
devPositiveCount = 0
positive_perplexity = 0.0
prevWord = "<unk>"
for line in open(posselected):
	line.rstrip()
	tokens = line.split()
	for t in tokens:
		devPositiveCount += 1
		#replace unknown words with unk probability
		if t not in bigram_pos:
			t = "<unk>" #REPLACE UNKNOWNS WITH UNK
		if t not in bigram_pos[prevWord][0]:
			#use smoothed count for probability for <prevWord, t>
			p = k / (uni_counts_pos[prevWord]+(k*len(uni_counts_pos)))
		else:
			i = bigram_pos[prevWord][0].index(t)
			p = bigram_pos[prevWord][1][i]
		positive_perplexity -= math.log(p)
		prevWord = t 

positive_perplexity = positive_perplexity / devPositiveCount #summation / N
positive_perplexity = math.exp(positive_perplexity)
print("Positive perplexity: " + str(positive_perplexity))


# NOW FOR NEGATIVE PERPLEXITY 

#keys are first token of bigram, values are ([second words of token], [corresponding number of appearances]) tuples
count_neg = {}
uni_counts_neg = {}
prob_neg = [] 
tokencount = 0
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
        tokencount+=1
    tokencount +=1
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

totalprob = 0
for key in bigram_neg:
	for p in bigram_neg[key][1]:
		totalprob+=p
#PEREPLXITY]
devnegativeCount = 0
negative_perplexity = 0.0
prevWord = "<unk>"
for line in open(negselected):
	line.rstrip()
	tokens = line.split()
	for t in tokens:
		devnegativeCount += 1
		#replace unknown words with unk probability
		if t not in bigram_neg:
			t = "<unk>" #REPLACE UNKNOWNS WITH UNK
		if t not in bigram_neg[prevWord][0]:
			#use smoothed count for probability for <prevWord, t>
			p = k / (uni_counts_neg[prevWord]+(k*len(uni_counts_neg)))
		else:
			i = bigram_neg[prevWord][0].index(t)
			p = bigram_neg[prevWord][1][i]
		negative_perplexity -= math.log(p)
		prevWord = t 

negative_perplexity = negative_perplexity / devnegativeCount #summation / N
negative_perplexity = math.exp(negative_perplexity)
print("Negative perplexity: " + str(negative_perplexity))
