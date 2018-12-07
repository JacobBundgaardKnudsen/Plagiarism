###### Warning ######
Do not run the DownloadWikiArticles.py before testing the CheckFile.py script.
The reason is that the current testfiles located in testDocuments are custom made to test for plagiarism in the pre downloaded Wikipedia pages.


In order to run the scripts several packages are needed:
SpaCy2, gensim, pickle, mmh3, termcolor



DownloadWikiArticles.py
This script does not take any inputs.
it downloads 100 random Wikipedia articles into the WikiPages folder

python DownloadWikiArticles.py



PlagiarismDetection.py
This script does not take any inputs
Within the script the length of shingles, number of Minhashes and number of buckets can be changed.

python PlagiarismDetection.py


CheckFile.py
The script takes up to two arguments. The first being the document which should be tested and the second is an optional threshold to the Jaccard similarity.

Within the script the length of shingles, number of Minhashes and number of buckets can be changed.

python PlagiarismDetection.py "suspicious document.txt"

Other text documents can be found in "testDocuments
