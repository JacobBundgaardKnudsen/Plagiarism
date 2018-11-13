import sys
import os
import mmh3


#################### Utilities ######################
#hashes a list of strings
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

def signatures(docs, q, k):
    for file_name, text in docs.items():
        docs[file_name] = minhash(ngram(q, text), k)

def jaccard(Ssig,Tsig):
    k = len(Ssig)
    eq = 0
    for i in range(0,k):
        if Ssig[i] == Tsig[i]:
            eq += 1
    return eq/k  


################### Similarity ######################
q = 3 # length of shingle
k = 100 # number of minhashes
docs = {} #dictionary mapping document id to document contents

# read data sets
srcfolder = os.path.dirname(os.path.abspath(__file__))
datafolder = os.path.join(srcfolder, "ats_corpus_small")   # change to ats_corpus for large data set

for file in os.listdir(datafolder):
    filepath = os.path.join(datafolder, file)
    f = open(filepath, 'r')
    docs[file] = f.read()
    print("read document " + file)
    f.close()

signatures(docs, q, k)
#print(docs_signatures.values())

for key, value in docs.items():
    for other_key, other_value in docs.items():
        if key != other_key:
            result = jaccard(value, other_value)
            #print(key + " and " + other_key + " value: " + str(result))
            if(result >= 0.6):
                print(key + " and " + other_key + "are similar with a value of: " + str(result))