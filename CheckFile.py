import sys
import mmh3
import inspect, os
import pickle
from collections import defaultdict
from termcolor import colored
from gensim.parsing import preprocessing as genPreProc
from gensim.parsing.preprocessing import preprocess_string
from spacy import load

#loads a textfile
def loadDoc(dataPath):
    with open(dataPath, encoding="utf8", errors='ignore') as loadedDoc:
        doc = loadedDoc.read()
    return doc

#Hashes a list
def listhash(l,seed): 
    val = 0
    for e in l:
        val = val ^ mmh3.hash(e, seed)
    return val 

#create shingles
def ngram(shingle_length, string):
    tokens = string.split()
    shingles = [tokens[i:i+shingle_length] for i in range(len(tokens) - shingle_length + 1)]
    
    return shingles

#finds the minimum hashvalue
def minhash(shingles, k):
    min_hashes = [sys.maxsize] * k
    for i in range(k):
        for shingle in shingles:
            shingle_hash = listhash(shingle, i)
            if(shingle_hash < min_hashes[i]):
                min_hashes[i] = shingle_hash
    return min_hashes

#processes the input text
def preprocessing(filename, folder):
    nlp = load('en')
    
    #chosing the target folder and loading the selected file
    srcfolder = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    datafolder = os.path.join(srcfolder, folder) 
    filepath = os.path.join(datafolder, filename)
    document = loadDoc(filepath)

    sentenceSplit = list(nlp(document).sents) #splits a text into sentences
    gensimSettings = [lambda x: x.lower(), genPreProc.remove_stopwords, genPreProc.stem,
                        genPreProc.strip_non_alphanum, genPreProc.strip_multiple_whitespaces]
    sentencePreprocess = [' '.join(preprocess_string(str(sentence), filters=gensimSettings)) for sentence in sentenceSplit]

    return sentencePreprocess

#calculates the jaccard similarity
def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    if (union == 0):
        return 1
    else:
        return float(intersection / union)
    

def checkfileSentence(filename, b, k, M, q):
    textFile = preprocessing(filename, "testDocuments") #loading the text with preprocessing
    
    similarDocs = set([])
    r = int(k/b)
    signatures = []

    for sentence in textFile:
        signatures.append(minhash(ngram(q, sentence), k)) #creating a signature for each sentence
    
    for signature in signatures:
        for band in range(0, k, r):
            index = int(band/r)
            signatureBand = tuple(signature[band:band+r]) #selecting the bucket
            sentenceName = filename + '_' + str(signatures.index(signature)) + '_' + str(len(signatures)) #creating the value in the dict with the appropriate information
            if signatureBand in M[index]:
                for item in M[index][signatureBand]:
                    similarDocs.add((sentenceName,item)) #saving the document information in the dictionary under the correct bucket

    return similarDocs

#Different degrees of plagiarism
def degree(value):
    if value == 0:
        return "none"
    elif value <= 10:
        return "low"
    elif value <= 50:
        return "medium"
    else:
        return "high"

#output colors
colors = {
    "none":"green",
    "low":"yellow",
    "medium":"red",
    "high":"magenta"
}

#unpacking data, used when loading dump
def unpack_file_data(file):
    data = file.split("_")
    name = data[0]
    sentence = data[-2]
    count = data[-1]
    return (name, sentence, count)


#formating text and printing the correct output
def display(testFile, similarFiles=[], threshold=0.8):
    testDocument = preprocessing(testFile, "testDocuments") #loading file

    sentenceCount = len(testDocument)
    foundInstances = len(similarFiles)
   
    plagiarismDegree = 0

    if foundInstances > 0:
        plagiarismDegree = (foundInstances/sentenceCount) * 100
    print("\nOverall result of the analysis\n")
    print(colored("Plagiarism degree: " + degree(plagiarismDegree), colors[degree(plagiarismDegree)]), end="\n\n")

    if similarFiles:
        print("similar files have been found")

        groupedFiles = defaultdict(list)
        sentenceCount = 0

        #unpacking the files
        for fileName in similarFiles:
            testFile, testSentence, testLength = unpack_file_data(fileName[0])
            corpusFile, corpusSentence, corpusLength = unpack_file_data(fileName[1])
            groupedFiles[corpusFile].append((testSentence, corpusSentence))
        
        for fileName, sentences in groupedFiles.items():            
            document = preprocessing(fileName, "WikiPages")

            for testSentence, corpusSentence in sentences:
                testNgram = ngram(3, testSentence)
                matchingNgram = ngram(3, corpusSentence)
                jaccardSim = jaccard_similarity([tuple(elem) for elem in matchingNgram], [tuple(elem) for elem in testNgram])

                if (jaccardSim >= threshold): #checking that the jaccard is high enough
                    sentenceCount += 1
                    print("____________ " + str(sentenceCount) + " of " + str(len(similarFiles)) + " ____________", end='\n\n')
                    print("sentence " + testSentence + " in the test document:", end=" ")
                    print(colored(testDocument[int(testSentence)], "cyan"), end="\n\n")
                    print("was found in sentence " + corpusSentence + " in document " + fileName + ":", end=" ")
                    print(colored(document[int(corpusSentence)], "blue"), end="\n\n")

q = 3 # length of shingle
k = 50 # number of minhashes
b = 10 # number of bands

with open("LSHDict", "rb") as file:
    LSHDict = pickle.load(file)

testDocument = sys.argv[1]
output = checkfileSentence(testDocument, b, k, LSHDict, q)

#Checks if the user provided 1 or 2 arguments
if len(sys.argv) >= 3:
    threshold = float(sys.argv[2])
    display(testDocument, list(output), threshold)
else:
    display(testDocument, list(output))