import numpy
import regex
import os

pos = "Project1/SentimentDataset/Train/pos.txt"
neg = "Project1/SentimentDataset/Train/neg.txt"
pospre = "Project1/SentimentDataset/Train/pospre.txt"
negpre = "Project1/SentimentDataset/Train/negpre.txt"
k = .16
#preprocessing, add start marks and end marks, change all letters to lower case
f1 = open(pospre,"w")
for line in open(pos):
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

f2 = open(negpre,"w")
for line in open(neg):
    line.rstrip()
    tokens = line.split()
    newL = " <s> "
    for t in tokens:
        if t=="''" or t=="'" or t[0] == "`" or t[0] == '\\':
            continue 
        else:
            newL += t + " "
    newL += " </s>\n"
    newL = newL.lower()
    f2.write(newL)
f2.close()

## new bigram table -----------------------------------------------------------------------------------------------
#keys are first token of bigram, values are ([second words of token], [corresponding number of appearances]) tuples
count_pos = {}
uni_counts_pos = {}
prob_pos = [] 
for line in open(pospre):
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
for c in count_pos:
    bigram_pos[c] = ([], []) #tuple is ([list of words], [corresponding P(word | c) values])
    for i,x in enumerate(count_pos[c][1]):
        word = count_pos[c][0][i]
        bigram_pos[c][0].append(word)
        bigram_pos[c][1].append((x+k) / (uni_counts_pos[word]+(k*len(uni_counts_pos)))) #Count(w_n-1 w_n) / count(w_n-1)
    sumP = sum(bigram_pos[c][1])
    for i,x in enumerate(bigram_pos[c][1]):
        bigram_pos[c][1][i] = x / sumP

punctuation = [",",".","!","?",":",";"]
#generate 10 random sentences using P(W_n | w_n-1) = Count(w_n-1 w_n) / count(w_n-1)
print("POSITIVE TEXT:")
for _ in range(10):
    line = ""
    #start with <s>
    nextChar = numpy.random.choice(bigram_pos["<s>"][0], None, True, bigram_pos["<s>"][1])
    while nextChar != "</s>":
        if (line == "" or line[-1] in punctuation) and (nextChar[-1] in punctuation or nextChar[-1] == "-"):
            pass
        elif (line == "" or len(line) < 2 or line[-1] == ".") and nextChar[-1] not in punctuation:
            line += " " + nextChar.title()
        elif "'" in nextChar:
            line += nextChar
        elif nextChar[-1] not in punctuation:
            line += " " + nextChar
        else:
            line += nextChar
        prevChar = nextChar
        nextChar = numpy.random.choice(bigram_pos[prevChar][0], None, True, bigram_pos[prevChar][1])
    print(line)

#now for negative
count_neg = {}
uni_counts_neg = {}
prob_neg = [] 
for line in open(negpre):
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
for c in count_neg:
    bigram_neg[c] = ([], []) #tuple is ([list of words], [corresponding P(word | c) values])
    for i,x in enumerate(count_neg[c][1]):
        word = count_neg[c][0][i]
        bigram_neg[c][0].append(word)
        bigram_neg[c][1].append((x+k) / (uni_counts_neg[word]+(k*len(uni_counts_neg)))) #Count(w_n-1 w_n) / count(w_n-1)

    sumP = sum(bigram_neg[c][1])
    for i,x in enumerate(bigram_neg[c][1]):
        bigram_neg[c][1][i] = x / sumP

print("NEGATIVE TEXT:")
#generate 10 random sentences using P(W_n | w_n-1) = Count(w_n-1 w_n) / count(w_n-1)
for _ in range(10):
    line = ""
    #start with <s>
    nextChar = numpy.random.choice(bigram_neg["<s>"][0], None, True, bigram_neg["<s>"][1])
    while nextChar != "</s>":
        if (line == "" or line[-1] in punctuation) and (nextChar[-1] in punctuation or nextChar[-1] == "-"):
            pass
        elif (line == "" or len(line) < 2 or line[-1] == "." or line[-1] == "!" or line[-1] == "?") and nextChar[-1] not in punctuation:
            line += " " + nextChar.title()
        elif "'" in nextChar:
            line += nextChar
        elif nextChar[-1] not in punctuation:
            line += " " + nextChar
        else:
            line += nextChar
        prevChar = nextChar
        nextChar = numpy.random.choice(bigram_neg[prevChar][0], None, True, bigram_neg[prevChar][1])
    print(line)

# end new bigram table --------------------------------------------------------------------------------
