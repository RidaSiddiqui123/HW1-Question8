#-------------------------------------------------------------------------
# AUTHOR: Rida Siddiqui
# FILENAME: search_engine.py
# SPECIFICATION: Ouput precision and recall of a search engine given a query
# FOR: CS 4250- Assignment #1
# TIME SPENT: 1 hr
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#importing some Python libraries

#read the file collection.csv and
#output the precision/recall of a proposed search engine given the query q ={cat and dogs}

import csv
import math
documents = []
labels = []

#reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])
            labels.append(row[1])
         #print(documents)
         #print(labels)

#Conduct stopword removal.
#--> add your Python code here
stopWords = {'I', 'and', 'She', 'They', 'her', 'their'}
goodWords = []
for i, words in enumerate(documents):
    g = words.replace('I', '').replace('and', ''). replace('She', '').replace('They', '').replace('her', '').replace('their', '').split()
    goodWords.append(g)



#Conduct stemming.
#--> add your Python code here
stemming = {
  "cats": "cat",
  "dogs": "dog",
  "loves": "love",
}

stemmedWords = []
terms = []
for i, string in enumerate(goodWords):
    paper =[]
    for j, word in enumerate(string):
        if word in stemming: #not in paper:
            paper.append(stemming[word])
        if word not in stemming:
            paper.append(word)

    stemmedWords.append(paper)
print("Documents after stop-word removal and stemming:")
print(stemmedWords)


#Identify the index terms.
#--> add your Python code here
terms = []
#to comment code out: ctrl /
for i, string in enumerate(stemmedWords):
    for j, word in enumerate(string):
        if word not in terms:
            terms.append(word)


#Build the tf-idf term weights matrix.
#--> add your Python code here
idf = 0
tfList = []
idfList = []
binaryList1 = []
for i, term in enumerate(terms):
    tfWordList = []
    inDocuments = 0
    binaryList = []
    for j, string in enumerate(stemmedWords):
        count = string.count(term)
        tfWordList.append(count/len(string))

        if count != 0:
            inDocuments = inDocuments+1
            binary = 1
        else:
            binary = 0
        binaryList.append(binary)

    binaryList1.append(binaryList)
    tfList.append(tfWordList)
    idf = math.log(len(stemmedWords) / inDocuments, 10)
    idfList.append(idf)

tf_idfList = []
for i, tfWord in enumerate(tfList):
    tf_idfTempList = []
    for j, tf in enumerate(tfWord):
        tf_idf = tf * idfList[i]
        tf_idfTempList.append(tf_idf)
    tf_idfList.append(tf_idfTempList)

print()
print("tf-idf term weights matrix:")
       #list = [[0, 0, 0], [0.5, 0.4, 0], [0.4, 0.3, 0.5]]

print("                 %s     %s     %s" % (terms[0], terms[1], terms[2]))

#Calculate the document scores (ranking) using document weigths (tf-idf) calculated before and query weights (binary - have or not the term).
#--> add your Python code here
docMatrix = []
docScores = []

for i, tf_idf in enumerate(tf_idfList):
    print("Document %d" % (i+1), end = "    ")
    docList = []
    dotProduct = 0
    sum = 0
    for j, tf_idf2 in enumerate(tf_idfList):
        print("  %.4f" % (tf_idfList[j][i]), end = " ")
        docList.append(tf_idfList[j][i])
        #print("binrary")
       # print(binaryList1[j][i])
        product = tf_idfList[j][i] * binaryList1[j][i]
        #print("product")
        #print(product)
        sum = sum + product

        #print(docList)
    #print("sum")
    #print(sum)
    docScores.append(sum)
    docMatrix.append(docList)
    print("")

print("")
print("Document Scores: " + str(docScores))
#print("docMatrix: " + str(docMatrix))

#Calculate and print the precision and recall of the model by considering that the search engine will return all documents with scores >= 0.1.
#--> add your Python code here

a =0 # hits
b= 0
c=0
for i, score in enumerate(docScores):
    if score >= 0.1: #if document is retreieved
        if labels[i] == ' R': #check if document is relevant
            a = a+1
        if labels[i] == ' I': #check if document is irrelevant
            b = b+1
    if score < 0.1: #check if document is not retreived
        if labels[i] == ' R':
            c = c+1

precision = (a/(a+b)) * 100
recall = (a/(a+c)) * 100
print()
print("Precision: " + str(precision) + "%")
print("Recall: " + str(recall) + "%")