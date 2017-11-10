#by Runqian Huang      Sep/10th/2017
import numpy

pos = "Project1\SentimentDataset\Train\pos.txt"
neg = "Project1\SentimentDataset\Train\\neg.txt"
pospre = "Project1\SentimentDataset\Train\pospre.txt"
negpre = "Project1\SentimentDataset\Train\\negpre.txt"

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

#creating bigram tables
postemp=[]
postype=0   #number of word types
postoken=0  #number of word tokens
for line in open(pospre):
	line.rstrip()
	tokens = line.split()
	for word in tokens:
		postemp.append(word)
#print(postemp)
postempnp=numpy.array(postemp)
#print(postempnp)
postoken=postempnp.size
#print(postoken)
postemp2=[]
postemp2.append(postempnp[0])
postemp2.append(postempnp[1])
postype=2
for i in range(0,postoken):
    tag=0
    for j in range(0,postype):
        if postemp2[j]!=postempnp[i]:
            j=j+1
            tag=j
        else:
            break
    if tag==postype:
        postemp2.append(postempnp[i])
        postype=postype+1
    i=i+1
print(postemp2)
postable=numpy.array(postemp2)
#print(postype)

negtemp=[]
negtype=0   #number of word types
negtoken=0  #number of word tokens
for line in open(negpre):
	line.rstrip()
	tokens = line.split()
	for word in tokens:
		negtemp.append(word)
#print(negtemp)
negtempnp=numpy.array(negtemp)
#print(negtempnp)
negtoken=negtempnp.size
#print(negtoken)
negtemp2=[]
negtemp2.append(negtempnp[0])
negtemp2.append(negtempnp[1])
negtype=2
for i in range(0,negtoken):
    tag=0
    for j in range(0,negtype):
        if negtemp2[j]!=negtempnp[i]:
            j=j+1
            tag=j
        else:
            break
    if tag==negtype:
        negtemp2.append(negtempnp[i])
        negtype=negtype+1
    i=i+1
print(negtemp2)
negtable=numpy.array(negtemp2)
#print(negtype)
