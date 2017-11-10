import numpy
import math
import regex
import os

posunk = "Project1/SentimentDataset/Train/posunk.txt"
negunk = "Project1/SentimentDataset/Train/negunk.txt"
posselected = "Project1/SentimentDataset/Dev/unigrampositive.txt"
negselected = "Project1/SentimentDataset/Dev/unigramnegative.txt"
k = .28

#build probability model
count_pos = {} 
prob_pos = []
length_pos = 0
for line in open(posunk):
	line.rstrip()
	tokens = line.split()
	for t in tokens:
		if t=="<s>":
			continue #ignore <s> for unigram
		length_pos += 1
		if t in count_pos:
			count_pos[t] += 1 
		else:
			count_pos[t] = 1
posWords = list(count_pos.keys())
for key in posWords:
	probability = (count_pos[key]+k) / (length_pos+(k*len(posWords)))
	prob_pos.append(probability)
	count_pos[key] = probability

#PEREPLXITY
devPositiveCount = 0
positive_perplexity = 0.0
for line in open(posselected):
	line.rstrip()
	tokens = line.split()
	for t in tokens:
		devPositiveCount += 1
		#replace unknown words with unk probability
		if t not in count_pos:
			t = "<unk>"
		positive_perplexity -= math.log(count_pos[t])

positive_perplexity = positive_perplexity / devPositiveCount #summation / N
positive_perplexity = math.exp(positive_perplexity)
print("Positive perplexity: " + str(positive_perplexity))

#build probability model
k = .1
count_neg = {} 
prob_neg = {}
length_neg = 0
for line in open(negunk):
	line.rstrip()
	tokens = line.split()
	for t in tokens:
		if t=="<s>":
			continue #ignore <s> for unigram
		length_neg += 1
		if t in count_neg:
			count_neg[t] += 1 
		else:
			count_neg[t] = 1
negWords = list(count_neg.keys())
for key in negWords:
	probability = (count_neg[key]+k) / (length_neg+(k*len(negWords)))
	prob_neg[key] = probability

#PEREPLXITY
devnegativeCount = 0
negative_perplexity = 0.0
for line in open(negselected):
	line.rstrip()
	tokens = line.split()
	for t in tokens:
		devnegativeCount += 1
		#replace unknown words with unk probability
		if t not in prob_neg:
			t = "<unk>"
		negative_perplexity -= math.log(prob_neg[t])

negative_perplexity = negative_perplexity / devnegativeCount #summation / N
negative_perplexity = math.exp(negative_perplexity)
print("Negative perplexity: " + str(negative_perplexity))


