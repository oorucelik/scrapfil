import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import numpy as np
from time import sleep
from random import randint
name = 'oorucelik'
r = requests.get('https://www.sinefil.com/%s/films/watched'%name)
soup = BeautifulSoup(r.content,'lxml')
movie_div = soup.find_all('div',attrs={'class':['movie','movie first']})
types = []
images = []
titles = []
durations = []
releaseDates = []
imdbScores = []
genres = []

filmCount=0
tvseriesCount=0
pagesFilms= int(soup.find('div',attrs={'class':'pagination right'}).text[10:12])
print(pagesFilms)
#films
for page in range(2,pagesFilms+2):
    countPage=0
    for i,container in enumerate(movie_div) :
        countPage+=1
        #type
        types.append("film")
        #title
        if(container.find_all('div',attrs={'class':'mini-hero'})[0].text.strip()==''):
            title=container.h3.a.text
        else:
            title=container.find_all('div',attrs={'class':'mini-hero'})[0].text.strip()
        titles.append(title)
        #releaseDate #- duration - genre
        rowList = container.table.find_all('tr')
        initialList = []
        for _, row in enumerate(rowList):
            rowInitial= row.text.strip()[0]
            initialList.append(rowInitial)
            textRight = row.find('td',attrs={'text-right'}).text.strip()
            if rowInitial == "V":
                releaseDates.append(textRight)
            elif rowInitial == "S":
                durations.append(textRight)
            elif rowInitial == "T":
                genres.append(textRight.replace("\n",", "))
        if len(initialList)!=3:
            if "V" not in initialList:
                releaseDates.append(container.h3.span.text[2:-1])
            elif "S" not in initialList:
                releaseDates.append("-")
            elif "T" not in initialList:
                releaseDates.append("-")
        #imdbScore
        scoresTable = container.find_all('span',attrs={'class':'count'})

        if len(scoresTable)==0:
            imdbScores.append('-')
        else:
            for _ in scoresTable:
                if len(scoresTable)>1:
                    imdbScores.append(scoresTable[1].text) 
                    break
                else:
                    imdbScores.append(scoresTable[0].text)
        #images
        images.append(container.img['data-src'])
    filmCount+=countPage
    print('Page %d/%d is done. %d/%d Films'%(page-1,pagesFilms,countPage,filmCount))
    sleep(randint(2,3))
    r = requests.get('https://www.sinefil.com/%s/films/watched/%d'%(name,page))
    soup = BeautifulSoup(r.content,'lxml')
    movie_div = soup.find_all('div',attrs={'class':['movie','movie first']})

    
myMovies = pd.DataFrame({
'Type':types,
'Titles':titles,
'Duration':durations,
'Release Date':releaseDates,
'IMDB Score':imdbScores,
'Genre':genres,
'Image':images,})

totalCounts = pd.DataFrame({'filmCount':filmCount},index=[0])

# Creating Excel Writer Object from Pandas  
myMovies.to_excel('movies.xlsx')   
totalCounts.to_excel('totals.xlsx')
