import wikipedia
import random
import pickle
import os
import inspect

srcfolder = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
datafolder = os.path.join(srcfolder, "WikiArticles")   # change to ats_corpus for large data set (ats_corpus_small)

blackList = ["_", "(", ")", "/", "\\"]
numberOfArticles = 0

while numberOfArticles <= 100:
#for x in range(0,100):
    try:
        page = wikipedia.page(pageid = random.randint(1000,10000))
        if not any(elem in page.title for elem in blackList):
            content = page.content.replace("\n","")

            with open(datafolder + "/" + page.title + ".txt", "wb") as file:
                pickle.dump(content, file)
            numberOfArticles += 1
            
    except Exception as e:
        print(numberOfArticles, e)