from nltk.tokenize import word_tokenize
#use text files without newline characters
posTxt = "Project1/SentimentDataset/Train/pos.txt"
negTxt = "Project1/SentimentDataset/Train/neg.txt"
test = "Project1/SentimentDataset/Test/test.txt"
#generate tokens for pos
f = open(posTxt)
raw = f.read()
tokens = word_tokenize(raw)
print(type(tokens))
print(len(tokens))

posTokens = open("Project1/positiveTokens", 'w')
for t in tokens:
	posTokens.write(t+" ")

f = open(negTxt)
raw = f.read()
tokens = word_tokenize(raw)
print(type(tokens))
print(len(tokens))

negTokens = open("Project1/negativeTokens", 'w')
for t in tokens:
	negTokens.write(t+" ") #write token plus whitespace

f = open(test)
raw = f.read()
tokens = word_tokenize(raw)
print(type(tokens))
print(len(tokens))

testTokens = open("Project1/testTokens", 'w')
for t in tokens:
	testTokens.write(t+" ")
