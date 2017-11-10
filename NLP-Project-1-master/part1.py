#Preprocessing:
#Remove quotation marks
#Make everything lowercase
#remove tokens starting with '` for unigram
#for bigram we will have to merge things like 's with the word that came before it
#insert start and end tokens
# use numpy.random.choice
import numpy

pos = "Project1\SentimentDataset\Train\pos.txt"
neg = "Project1\SentimentDataset\Train\pos.txt"
pospre = "Project1/SentimentDataset/Train/pospre1.txt"
negpre = "Project1/SentimentDataset/Train/negpre1.txt"

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

#unigram for positive
count_pos = {} 
prob_pos = []
length_pos = 0
for line in open(pospre):
	line.rstrip()
	tokens = line.split()
	for t in tokens:
		length_pos += 1
		if t in count_pos:
			count_pos[t] += 1 
		else:
			count_pos[t] = 1
posWords = list(count_pos.keys())
for key in posWords:
	prob_pos.append(count_pos[key] / length_pos)

#unigram for negative
count_neg = {}
prob_neg = []
length_neg = 0
for line in open(negpre):
	line.rstrip()
	tokens = line.split()
	for t in tokens:
		length_neg += 1
		if t in count_neg:
			count_neg[t] += 1 
		else:
			count_neg[t] = 1
negWords = list(count_neg.keys())
for key in negWords:
	prob_neg.append(count_neg[key] / length_neg)

punctuation = [",",".","!","?",":"]
#positive sentence generation
print("POSITIVE SENTENCES: ")
for _ in range(10):
	line = ""
	nextChar = numpy.random.choice(posWords, None, True, prob_pos)
	while nextChar != "</s>":
		if (line == "" or line[-1] in punctuation) and (nextChar[-1] in punctuation or nextChar[-1] == "-"):
			pass
		elif (line == "" or len(line) < 2 or line[-1] == "." or line[-1] == "!" or line[-1] == "?") and nextChar[-1] not in punctuation:
			line += " " + nextChar.title()
		elif nextChar[-1] not in punctuation:
			line += " " + nextChar
		else:
			line += nextChar
		nextChar = numpy.random.choice(posWords, None, True, prob_pos)
	print(line)
print("\n")

#negative sentence generation 
print("NEGATIVE SENTENCES: ")
for _ in range(10):
	line = ""
	nextChar = numpy.random.choice(negWords, None, True, prob_neg)
	while nextChar != "</s>":
		if (line == "" or line[-1] in punctuation) and (nextChar[-1] in punctuation or nextChar[-1] == "-"):
			pass
		elif (line == "" or len(line) < 2 or line[-1] == "." or line[-1] == "!" or line[-1] == "?") and nextChar[-1] not in punctuation:
			line += " " + nextChar.title()
		elif nextChar[-1] not in punctuation:
			line += " " + nextChar
		else:
			line += nextChar
		nextChar = numpy.random.choice(negWords, None, True, prob_neg)
	print(line)
print("\n")