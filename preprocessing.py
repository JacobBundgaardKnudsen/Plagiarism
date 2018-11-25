import os
from gensim.parsing import preprocessing as genPreProc
from gensim.parsing.preprocessing import preprocess_string
from spacy import load

nlp = load('en')

dir = r"C:\Users\DavidStudie\OneDrive\Davids_doc\DTU\13th_Semester\02807_ComputationalToolsforDataScience\Project\Plagiarism\localitysensitivehashing\ats_corpus_small"
fileName = r"lifeofrevrichard00baxt.txt"
dataPath = dir+'\\'+fileName

class preprocessingPlag:
    # this function should:
    # - load text in a list (DONE)
    # - remove stop words
    # - stem the text
    # - remove punctuation
    # - keep numbers and keep everything lowercase
    # initialize preprocessing class
    def __init__(self, dataPath):
        if os.path.exists(dataPath):
            self.document = self.loadDoc(dataPath)

            genSettings = [lambda x: x.lower(), genPreProc.remove_stopwords,
                           genPreProc.stem, genPreProc.strip_multiple_whitespaces,
                           genPreProc.strip_non_alphanum, genPreProc.strip_punctuation]
            self.gensimPreprocess = ' '.join(preprocess_string(self.document, filters=genSettings))

            genSettings2 = [lambda x: x.lower(), genPreProc.remove_stopwords, genPreProc.stem]
            step1preprocess = ' '.join(preprocess_string(self.document, filters=genSettings2))
            sentenceSplit = list(nlp(step1preprocess).sents)
            genSettings3 = [lambda x: genPreProc.strip_non_alphanum(x), genPreProc.strip_multiple_whitespaces]
            sentencePreprocess = [' '.join(preprocess_string(str(ite), filters=genSettings3)) for ite in sentenceSplit]
            self.sentencePreprocess = {os.path.basename(dataPath): sentencePreprocess}

        else:
            print("\n\npath or file does not exist:\n  %s" % dataPath)
            pass

    def loadDoc(self, dataPath):
        with open(dataPath, 'r') as loadedDoc:
            doc = loadedDoc.read().replace('\n', '')
        with open(dataPath, 'r') as foo:
            test = ''.join([line for line in foo]).replace('\n', '')
        return doc

docText = preprocessingPlag(dataPath)

print(docText.document)
print(docText.gensimPreprocess)
print(docText.sentencePreprocess)

