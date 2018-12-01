from __future__ import division

def degree(value):
    if value == 0:
        return "none"
    elif value <= 10:
        return "low"
    elif value <= 50:
        return "medium"
    else:
        return "high"

def display(testfile, sentenceCount, similarFiles=[]):
    foundInstances = len(similarFiles)
    plagiarismDegree = 0
    if foundInstances > 0:
        plagiarismDegree = (foundInstances/sentenceCount) * 100
    print("Plagiarism degree: " + degree(plagiarismDegree))

    if similarFiles:
        print("files")


display("ewer", 2)