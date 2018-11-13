from shingling import shingle
import sys
sentence = "This is a small sentence with and soem other"
shingles = shingle(3, sentence)
print(shingles)
# print(minhash(shingles, 2))

