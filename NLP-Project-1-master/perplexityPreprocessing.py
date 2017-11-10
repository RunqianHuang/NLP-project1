import numpy
import math 

pos = "Project1/SentimentDataset/Dev/pos.txt"
neg = "Project1/SentimentDataset/Dev/neg.txt"
unigrampospre = "Project1/SentimentDataset/Dev/unigrampositive.txt"
unigramnegpre = "Project1/SentimentDataset/Dev/unigramnegative.txt"
bigrampospre = "Project1/SentimentDataset/Dev/bigrampositive.txt"
bigramnegpre = "Project1/SentimentDataset/Dev/bigramnegative.txt"


f1 = open(unigrampospre,"w")
for line in open(pos):
    line.rstrip()
    tokens = line.split()
    newL = ""
    for t in tokens:
        if "'" in t or t[0] == "`" or t[0] == '\\':
            continue 
        else:
            newL += t + " "
    newL += "</s>\n"
    newL = newL.lower()
    f1.write(newL)
f1.close()

f2 = open(unigramnegpre,"w")
for line in open(pos):
    line.rstrip()
    tokens = line.split()
    newL = ""
    for t in tokens:
        if "'" in t  or t[0] == "`" or t[0] == '\\':
            continue 
        else:
            newL += t + " "
    newL += "</s>\n"
    newL = newL.lower()
    f2.write(newL)
f2.close()

f1 = open(bigrampospre,"w")
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

f2 = open(bigramnegpre,"w")
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

