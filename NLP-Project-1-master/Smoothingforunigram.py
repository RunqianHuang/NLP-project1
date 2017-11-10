#Preprocessing:
#Remove quotation marks
#Make everything lowercase
#remove tokens starting with '` for unigram
#for bigram we will have to merge things like 's with the word that came before it
#insert start and end tokens
# use numpy.random.choice
import numpy
import math

pos = "Project1\SentimentDataset\Train\pos.txt"
neg = "Project1\SentimentDataset\Train\pos.txt"
pospre = "Project1/SentimentDataset/Train/pospre1.txt"
negpre = "Project1/SentimentDataset/Train/negpre1.txt"
posunk = "Project1/SentimentDataset/Train/posunk.txt"
negunk = "Project1/SentimentDataset/Train/negunk.txt"
posselected = "Project1/SentimentDataset/Dev/pos.txt"
negselected = "Project1/SentimentDataset/Dev/neg.txt"
posselected1 = "Project1/SentimentDataset/Train/posselected.txt"
negselected1 = "Project1/SentimentDataset/Train/negselected.txt"

f1 = open(pospre,"w")
for line in open(pos):
	line.rstrip()
	tokens = line.split()
	newL = ""
	for t in tokens:
		if "'" in t or t[0] == "`" or t[0] == '\\':
			continue
		else:
			newL += t + " "
	newL += "</s> "
	newL = newL.lower()
	f1.write(newL)
f1.close()

f2 = open(negpre,"w")
for line in open(pos):
	line.rstrip()
	tokens = line.split()
	newL = ""
	for t in tokens:
		if "'" in t  or t[0] == "`" or t[0] == '\\':
			continue
		else:
			newL += t + " "
	newL += "</s> "
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

#unigram for positive and smoothing
count_pos = {}
prob_pos = []
length_pos = 0
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
	line.rstrip()
	tokens = line.split()
	for t in tokens:
		length_pos += 1
		if t in count_pos:
			count_pos[t] += 1
		else:
			count_pos[t] = 1
posWords = list(count_pos.keys())
posline = []
plsize = 0
for line in open(posselected):
    line.rstrip()
    tokens = line.split()
    for t in tokens:
        if t in posWords:
            posline.append(t)
        else:
            posline.append("<unk>")
        plsize += 1
maxpos = 0
posk = 0
for m in range(0,101):
    k = m/100
    for key in posWords:
        prob_pos.append( ( count_pos[key] + k ) / ( length_pos + k * Vpos ) )
    p = 0
    for j in range(0, plsize - 1):
        if posline[j] in posWords:
            p += math.log( ( count_pos[posline[j]] + k ) / ( length_pos + k * Vpos ) )  # Find unigrams
    if k == 0.00:
        maxpos = p
        posk = k
    else:
        if p > maxpos:
            maxpos = p
            posk = k
        #print(p)
print("k for pos-smoothing: ", posk)

#unigram for negative and smoothing
count_neg = {}
prob_neg = []
length_neg = 0
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
	line.rstrip()
	tokens = line.split()
	for t in tokens:
		length_neg += 1
		if t in count_neg:
			count_neg[t] += 1
		else:
			count_neg[t] = 1
negWords = list(count_neg.keys())
negline = []
nlsize = 0
for line in open(negselected):
    line.rstrip()
    tokens = line.split()
    for t in tokens:
        if t in negWords:
            negline.append(t)
        else:
            negline.append("<unk>")
        nlsize += 1
maxneg = 0
negk = 0
for m in range(0,101):
    k = m/100
    for key in negWords:
        prob_neg.append( ( count_neg[key] + k ) / ( length_neg + k * Vneg ))
    p = 0
    for j in range(0, nlsize - 1):
        if negline[j] in negWords:
            p += math.log( ( count_neg[negline[j]] + k ) / ( length_neg + k * Vneg ) )  # Find unigrams
    if k == 0.00:
        maxneg = p
        negk = k
    else:
        if p > maxneg:
            maxneg = p
            negk = k
        #print(p)
print("k for neg-smoothing: ", negk)

# using posselected and negselected as held-out data ------  k for pos-smoothing is 0.28   k for neg-smoothing is 0.1
# using posselected1 and negselected1 as held-out data ----  k for pos-smoothing is 1.0   k for neg-smoothing is 0.0
