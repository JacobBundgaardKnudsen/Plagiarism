from collections import defaultdict
from termcolor import colored

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
    "high":"mygenta"
}

print(colors["none"])

def unpack_file_data(file):
    data = file.split("_")
    name = data[0]
    sentence = data[-2]
    count = data[-1]
    return (name, sentence, count)

def tokenize(text):
    return text.split(".")[:-1]

def display(testFile, similarFiles=[]):

    testDocument = tokenize(open(testFile).read())
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
            document = tokenize(open(fileName).read())

            for testSentence, corpusSentence in sentences:
                sentenceCount += 1
                print("____________ " + str(sentenceCount) + " of " + str(len(similarFiles)) + " ____________", end='\n\n')
                print("sentence " + testSentence + " in the test document:", end=" ")
                print(colored(testDocument[int(testSentence)], "cyan"), end="\n\n")
                print("was found in sentence " + corpusSentence + " in document " + fileName + ":", end=" ")
                print(colored(document[int(corpusSentence)], "blue"), end='\n\n')

display("test.txt", [("test.txt_1_6", "a.txt_1_6"), ("test.txt_4_6", "b.txt_4_6"), ("test.txt_2_6", "b.txt_2_6)")])