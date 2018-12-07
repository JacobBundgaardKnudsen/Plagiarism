import sys
import mmh3
import inspect, os
import pickle
from gensim.parsing import preprocessing as genPreProc
from gensim.parsing.preprocessing import preprocess_string
from spacy import load

#loads a textfile
def loadDoc(dataPath):
    with open(dataPath, encoding="utf8", errors='ignore') as loadedDoc:
        doc = loadedDoc.read()
    return doc

#processes the input text
def preprocess(datafolder):
    docs = {}
    nlp = load('en')
    
    for file in os.listdir(datafolder): #going through all the files in the folder
        filepath = os.path.join(datafolder, file)
        if not file.startswith('.'):
            document = loadDoc(filepath)
            sentenceSplit = list(nlp(document).sents)
            gensimSettings = [lambda x: x.lower(), genPreProc.remove_stopwords, genPreProc.stem, #making the text uniform and removing stopwords
                              genPreProc.strip_non_alphanum, genPreProc.strip_multiple_whitespaces]
            sentencePreprocess = [' '.join(preprocess_string(str(sentence), filters=gensimSettings)) for sentence in sentenceSplit]

            docs[os.path.basename(filepath)] = sentencePreprocess
    return docs

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

#finds the minimum hashvalue
def signature(docs, q, k):
    docsSignature = {}
    for file_name, sentences in docs.items():
        signatures = []
        for sentence in sentences:
            signatures.append(minhash(ngram(q, sentence), k))
        docsSignature[file_name] = signatures
    return docsSignature

#creates a dictionary with with a subset of the signature as keys and the document sentences as value
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
k = 50 # number of minhashes
b = 10 # number of buckets

srcfolder = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
datafolder = os.path.join(srcfolder, "WikiPages")

docs = preprocess(datafolder)
docsSignature = signature(docs, q, k)
lshSentence(docsSignature, b, k)