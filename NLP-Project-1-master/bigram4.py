import numpy
import regex
import os

pos = "Project1/SentimentDataset/Train/pos.txt"
neg = "Project1/SentimentDataset/Train/neg.txt"
pospre = "Project1/SentimentDataset/Train/pospre.txt"
negpre = "Project1/SentimentDataset/Train/negpre.txt"

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
        bigram_pos[c][1].append(x / uni_counts_pos[word]) #Count(w_n-1 w_n) / count(w_n-1)
    sumP = sum(bigram_pos[c][1])
    for i,x in enumerate(bigram_pos[c][1]):
        bigram_pos[c][1][i] = x / sumP

punctuation = [",",".","!","?",":"]
#generate 10 random sentences using P(W_n | w_n-1) = Count(w_n-1 w_n) / count(w_n-1)
print("POSITIVE TEXT:")
for _ in range(10):
    line = ""
    #start with <s>
    nextChar = numpy.random.choice(bigram_pos["<s>"][0], None, True, bigram_pos["<s>"][1])
    while nextChar != "</s>":
        if (line == "" or line[-1] in punctuation) and (nextChar[-1] in punctuation or nextChar[-1] == "-"):
            pass
        elif (line == "" or len(line) < 2 or line[-1] == "." or line[-1] == "!" or line[-1] == "?") and nextChar[-1] not in punctuation:
            line += " " + nextChar.title()
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
        bigram_neg[c][1].append(x / uni_counts_neg[word]) #Count(w_n-1 w_n) / count(w_n-1)
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
        elif nextChar[-1] not in punctuation:
            line += " " + nextChar
        else:
            line += nextChar
        prevChar = nextChar
        nextChar = numpy.random.choice(bigram_neg[prevChar][0], None, True, bigram_neg[prevChar][1])
    print(line)

# end new bigram table --------------------------------------------------------------------------------


# posWords = list(count_pos.keys())
# for key in posWords:
#     prob_pos.append(count_pos[key] / length_pos)


# #creating bigram tables
# postemp=[]
# postype=0   #number of word types
# postoken=0  #number of word tokens
# for line in open(pospre):
#     line.rstrip()
#     tokens = line.split()
#     for word in tokens:
#         postemp.append(word)
# #print(postemp)
# postempnp=numpy.array(postemp)
# #print(postempnp)
# postoken=postempnp.size
# #print(postoken)
# postemp2=[]
# postemp2.append(postempnp[0])
# postemp2.append(postempnp[1])
# postype=2
# for i in range(0,postoken):
#     tag=0
#     for j in range(0,postype):
#         if postemp2[j]!=postempnp[i]:
#             j=j+1
#             tag=j
#         else:
#             break
#     if tag==postype:
#         postemp2.append(postempnp[i])
#         postype=postype+1
#     i=i+1
# ##print(postemp2)
# postable=numpy.array(postemp2)
# #print(postype)

# negtemp=[]
# negtype=0   #number of word types
# negtoken=0  #number of word tokens
# for line in open(negpre):
#     line.rstrip()
#     tokens = line.split()
#     for word in tokens:
#         negtemp.append(word)
# #print(negtemp)
# negtempnp=numpy.array(negtemp)
# #print(negtempnp)
# negtoken=negtempnp.size
# #print(negtoken)
# negtemp2=[]
# negtemp2.append(negtempnp[0])
# negtemp2.append(negtempnp[1])
# negtype=2
# for i in range(0,negtoken):
#     tag=0
#     for j in range(0,negtype):
#         if negtemp2[j]!=negtempnp[i]:
#             j=j+1
#             tag=j
#         else:
#             break
#     if tag==negtype:
#         negtemp2.append(negtempnp[i])
#         negtype=negtype+1
#     i=i+1
# ##print(negtemp2)
# negtable=numpy.array(negtemp2)
# negtype = type(negtable)




# ## bigram model for positive
# postable1 = regex.findall(r"\b\w+\s\w+", open(pospre).read(), overlapped=True)

# ## sort postable  
# len_postable = len(postable1)
# #print(len_postable)

# count_pos = [0 for i in range(len_postable)]
# #headcount_pos = [0 for i in range(length_pos)]

# prob_pos = [0 for i in range(len_postable)]
# size_postable = float(len_postable)

# headstr_pos = [' ' for i in range(len_postable)]
# tailstr_pos = [' ' for i in range(len_postable)]

# #count of each bigram combi
# for k in range(0 ,len_postable):
#     bistr = postable1[k]
# #    headstr_pos[k] = bistr.split(' ')[0]  # first word in kth bigram combination
# #    tailstr_pos[k] = bistr.split(' ')[0]  # second word in kth bigram combination 
#     #####unigram string stored : negWords = list(count_neg.keys())

# #   count bigram combi occurence    
#     with open(pospre) as postmp:
#         for line in postmp:
#             if bistr in line:
#                 count_pos[k] += 1

# #               unicount_pos[k] +=1
# #  count occurence of head word of bigram combi



# #probability of positive bigram combi
# for k in range(0 ,len_postable):
#     prob_pos[k] = count_pos[k]/size_postable
#   #  print(k,prob_pos[k],postable[k])

# temp=numpy.zeros((postype,postype))
# for i in range(0,postype):
#     for j in range(0,postype):
#         bistrtmp=postable[i]+' '+postable[j]
#         for k in range(0,len_postable):
#             if bistrtmp==postable1[k]:
#                 temp[i,j]=prob_pos[k]
# print(temp)

# ## bigram model for negative
# negtable = regex.findall(r"\b\w+\s\w+", open(negpre).read(), overlapped=True)
# len_negtable = len(negtable)
# #print(len_negtable)
# count_neg = [0 for i in range(len_negtable)]
# prob_neg = [0 for i in range(len_negtable)]
# size_negtable = float(len_negtable)

# #count of negative bigram combi
# for k in range(0 ,len_negtable):
#     bistr = negtable[k]
#     with open(negpre) as negtmp:
#         for line in negtmp:
#             if bistr in line:
#                 count_neg[k] += 1

# #probability of negative bigram combi
# for k in range(0 ,len_negtable):
#     prob_neg[k] = count_neg[k]/size_negtable
#     #print(k,prob_neg[k],negtable[k])



