import wikipedia
import random
import pickle
import os
import inspect

srcfolder = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
datafolder = os.path.join(srcfolder, "WikiPages") #defining output folder

blackList = ["_", "(", ")", "/", "\\"] #files with these symbols should not be included
numberOfArticles = 0

while numberOfArticles <= 100:
    try:
        page = wikipedia.page(pageid = random.randint(1000,10000)) #selecting a random wiki page
        if not any(elem in page.title for elem in blackList):
            content = page.content.replace("\n","") #removes new lines

            with open(datafolder + "/" + page.title + ".txt", "wb") as file:
                pickle.dump(content, file) #saves the file
            numberOfArticles += 1
            
    except Exception as e:
        print(numberOfArticles, e)