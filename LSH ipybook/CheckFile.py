import sys
import mmh3
import os
import inspect, os
import pickle
from gensim.parsing import preprocessing as genPreProc
from gensim.parsing.preprocessing import preprocess_string
from spacy import load
#from PlagiarismDetection import loadDoc, minhash, ngram

def loadDoc(dataPath):
    with open(dataPath, encoding="utf8", errors='ignore') as loadedDoc:
        doc = loadedDoc.read()#.replace('\n', '')
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
    print('document loaded')
    genSettings2 = [lambda x: x.lower(), genPreProc.remove_stopwords, genPreProc.stem]
    step1preprocess = ' '.join(preprocess_string(document, filters=genSettings2))
    sentenceSplit = list(nlp(step1preprocess).sents)

    genSettings3 = [lambda x: genPreProc.strip_non_alphanum(x), genPreProc.strip_multiple_whitespaces]
    sentencePreprocess = [' '.join(preprocess_string(str(ite), filters=genSettings3)) for ite in sentenceSplit]

    return sentencePreprocess

def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection / union)
    
def checkfileSentence(filename, b, k, M, q):
    textFile = preprocessing(filename, "testDocuments")

    print('preprocessing done')
    print("Looking for documents similar to " + filename)
    
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
            
    if len(similarDocs):
        print('Similar sentences')
        print(similarDocs)
    else:
        print("no similar sentences")
    
    for item in similarDocs:
        matchingSentenceInfo = item[1].split('_')
        matchingSentence = preprocessing(matchingSentenceInfo[0], "WikiPages")[int(matchingSentenceInfo[1])]
        matchingNgram = ngram(q, matchingSentence)
        


        testDocSentenceInfo = item[0].split('_')
        testDocSentence = preprocessing(testDocSentenceInfo[0], "testDocuments")[int(testDocSentenceInfo[1])]
        testNgram = ngram(q, testDocSentence)
    
        print(jaccard_similarity([tuple(elem) for elem in matchingNgram], [tuple(elem) for elem in testNgram]))

    return textFile



print("loading dict")
with open("LSHDict", "rb") as file:
    LSHDict = pickle.load(file)

print("dict loaded")

checkfileSentence('testDoc3.txt', 5, 100, LSHDict, 3)