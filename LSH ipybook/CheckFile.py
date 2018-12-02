import sys
import mmh3
import os
import inspect, os
import pickle
from collections import defaultdict
from termcolor import colored
from gensim.parsing import preprocessing as genPreProc
from gensim.parsing.preprocessing import preprocess_string
from spacy import load

def loadDoc(dataPath):
    with open(dataPath, encoding="utf8", errors='ignore') as loadedDoc:
        doc = loadedDoc.read()
    return doc

def listhash(l,seed): 
    val = 0
    for e in l:
        val = val ^ mmh3.hash(e, seed)
    return val 

def ngram(shingle_length, string):
    tokens = string.split()
    shingles = [tokens[i:i+shingle_length] for i in range(len(tokens) - shingle_length + 1)]
    
    return shingles

def minhash(shingles, k):
    min_hashes = [sys.maxsize] * k
    for i in range(k):
        for shingle in shingles:
            shingle_hash = listhash(shingle, i)
            if(shingle_hash < min_hashes[i]):
                min_hashes[i] = shingle_hash
    return min_hashes

def preprocessing(filename, folder):
    nlp = load('en')
    srcfolder = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    datafolder = os.path.join(srcfolder, folder)   # change to ats_corpus for large data set
    filepath = os.path.join(datafolder, filename)
    
    document = loadDoc(filepath)
    genSettings2 = [lambda x: x.lower(), genPreProc.remove_stopwords, genPreProc.stem]
    step1preprocess = ' '.join(preprocess_string(document, filters=genSettings2))
    sentenceSplit = list(nlp(step1preprocess).sents)

    genSettings3 = [lambda x: genPreProc.strip_non_alphanum(x), genPreProc.strip_multiple_whitespaces]
    sentencePreprocess = [' '.join(preprocess_string(str(ite), filters=genSettings3)) for ite in sentenceSplit]

    return sentencePreprocess

def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    if (union == 0):
        return 1
    else:
        return float(intersection / union)
    
def checkfileSentence(filename, b, k, M, q):
    textFile = preprocessing(filename, "testDocuments")
    
    similarDocs = set([])
    r = int(k/b)
    signatures = []
    for sentence in textFile:
        signatures.append(minhash(ngram(q, sentence), k))
    
    for signature in signatures:
        for band in range(0, k, r):      
            index = int(band/r)
            signatureBand = tuple(signature[band:band+r])
            sentenceName = filename + '_' + str(signatures.index(signature)) + '_' + str(len(signatures))
            if signatureBand in M[index]:
                for item in M[index][signatureBand]:
                    similarDocs.add((sentenceName,item))

    return similarDocs

########################################################################################################################################

def degree(value):
    if value == 0:
        return "none"
    elif value <= 10:
        return "low"
    elif value <= 50:
        return "medium"
    else:
        return "high"

colors = {
    "none":"green",
    "low":"yellow",
    "medium":"red",
    "high":"magenta"
}

def unpack_file_data(file):
    data = file.split("_")
    name = data[0]
    sentence = data[-2]
    count = data[-1]
    return (name, sentence, count)

def tokenize(text):
    return text.split(".")[:-1]

def display(testFile, similarFiles=[]):
    nlp = load('en')
    basePathCorpus = "./WikiPages/"
    basePathTest = "./testDocuments/"

    testDocument = list(nlp(open(basePathTest + testFile,encoding="utf8", errors='ignore').read()).sents)

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
        for fileName in similarFiles:
            testFile, testSentence, testLength = unpack_file_data(fileName[0])
            corpusFile, corpusSentence, corpusLength = unpack_file_data(fileName[1])
            groupedFiles[corpusFile].append((testSentence, corpusSentence))
        
        for fileName, sentences in groupedFiles.items():
            document = list(nlp(open(basePathCorpus + fileName,encoding="utf8", errors='ignore').read()).sents)

            for testSentence, corpusSentence in sentences:
                sentenceCount += 1
                print("____________ " + str(sentenceCount) + " of " + str(len(similarFiles)) + " ____________", end='\n\n')
                print("sentence " + testSentence + " in the test document:", end=" ")
                print(colored(testDocument[int(testSentence)], "cyan"), end="\n\n")
                print("was found in sentence " + corpusSentence + " in document " + fileName + ":", end=" ")
                print(colored(document[int(corpusSentence)+1], "blue"), end="\n\n")

                testNgram = ngram(3, testSentence)
                matchingNgram = ngram(3, corpusSentence)
                print("The Jaccard similarity is:",jaccard_similarity([tuple(elem) for elem in matchingNgram], [tuple(elem) for elem in testNgram]), end="\n\n")



with open("LSHDict", "rb") as file:
    LSHDict = pickle.load(file)

testDocument = "testDoc3.txt"

output = checkfileSentence(testDocument, 5, 100, LSHDict, 3)

display(testDocument, list(output))