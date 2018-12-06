import sys
import mmh3
import os
import inspect, os
import pickle
from gensim.parsing import preprocessing as genPreProc
from gensim.parsing.preprocessing import preprocess_string
from spacy import load
import time

time_start = time.clock()

def loadDoc(dataPath):
    with open(dataPath, encoding="utf8", errors='ignore') as loadedDoc:
        doc = loadedDoc.read()#.replace('\n', '')
    return doc

def preprocess(datafolder):
    docs = {}
    nlp = load('en')
    
    for file in os.listdir(datafolder):
        filepath = os.path.join(datafolder, file)
        if not file.startswith('.'):
            document = loadDoc(filepath)

            genSettings2 = [lambda x: x.lower(), genPreProc.remove_stopwords, genPreProc.stem]
            step1preprocess = ' '.join(preprocess_string(document, filters=genSettings2))
            sentenceSplit = list(nlp(step1preprocess).sents) #splitting document into sentences

            genSettings3 = [lambda x: genPreProc.strip_non_alphanum(x), genPreProc.strip_multiple_whitespaces]
            sentencePreprocess = [' '.join(preprocess_string(str(ite), filters=genSettings3)) for ite in sentenceSplit]

            docs[os.path.basename(filepath)] = sentencePreprocess
    return docs

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

def signature(docs, q, k):
    docsSignature = {}
    for file_name, sentences in docs.items():
        signatures = []
        for sentence in sentences:
            signatures.append(minhash(ngram(q, sentence), k))
        docsSignature[file_name] = signatures
    return docsSignature

def lshSentence(docsSignature, b, k):
    r = int(k/b)
    M = [{}]*b
    for name, signatures in docsSignature.items():
        for signature in signatures:
            for band in range(0, k, r):
                signatureBand = tuple(signature[band:band+r])
                index = int(band/r)
                sentenceName = name + '_' + str(signatures.index(signature)) + '_' + str(len(signatures))
                if tuple(signatureBand) not in M[index]:
                    M[index][signatureBand] = {sentenceName}
                else:
                    M[index][signatureBand].add(sentenceName)
                    
    with open("LSHDict", "wb") as file:
        pickle.dump(M, file)

q = 3 # length of shingle
k = 100 # number of minhashes
b = 5 # number of bands

srcfolder = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
datafolder = os.path.join(srcfolder, "WikiPages")   # change to ats_corpus for large data set (ats_corpus_small)

docs = preprocess(datafolder)
docsSignature = signature(docs, q, k)
lshSentence(docsSignature, b, k)

time_elapsed = (time.clock() - time_start)
print(time_elapsed)