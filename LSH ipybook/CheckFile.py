import sys
import mmh3
import os
import inspect, os
import pickle
from gensim.parsing import preprocessing as genPreProc
from gensim.parsing.preprocessing import preprocess_string
from spacy import load
from PlagiarismDetection import loadDoc, minhash, ngram

def checkfileSentence(filename, b, k, M, q):
    nlp = load('en')
    srcfolder = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    datafolder = os.path.join(srcfolder, "testDocuments")   # change to ats_corpus for large data set
    filepath = os.path.join(datafolder, filename)
    
    document = loadDoc(filepath)

    genSettings2 = [lambda x: x.lower(), genPreProc.remove_stopwords, genPreProc.stem]
    step1preprocess = ' '.join(preprocess_string(document, filters=genSettings2))
    sentenceSplit = list(nlp(step1preprocess).sents)

    genSettings3 = [lambda x: genPreProc.strip_non_alphanum(x), genPreProc.strip_multiple_whitespaces]
    sentencePreprocess = [' '.join(preprocess_string(str(ite), filters=genSettings3)) for ite in sentenceSplit]

    textFile = sentencePreprocess

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
    return textFile

with open("LSHDict", "rb") as file:
    LSHDict = pickle.load(file)

checkfileSentence('testDoc1.txt', 5, 100, LSHDict, 3)