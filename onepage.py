import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import numpy as np
from time import sleep
from random import randint
name = 'oorucelik'
types = []
images = []
titles = []
durations = []
releaseDates = []
imdbScores = []
genres = []

tvseriesCount=0
r = requests.get('https://www.sinefil.com/%s/tvseries/watched'%name)
soup = BeautifulSoup(r.content,'lxml')
tvseries_div= soup.find_all('div',attrs={'class':['movie','movie first']})
pagesTvseries= int(soup.find('div',attrs={'class':'pagination right'}).text[10:12])
#tvseries
for page in range(2,pagesTvseries+1):
    countPage=0
    for i,container in enumerate(tvseries_div) :
        countPage+=1
        #type
        types.append("Series")
        #title
        titleEnglish = container.find_all('div',attrs={'class':'mini-hero'})[0].text.strip()
        if(titleEnglish == ''):
            title = container.h3.a.text
        else:
            title = titleEnglish
        titles.append(title)
        
        #releaseYear
        releaseYear = container.h3.span.text[2:-1]
        if releaseYear !="":
            releaseDates.append(releaseYear)
        else:
            releaseDates.append("-")
        
        #duration - genre
        rowList = container.table.find_all('tr')
        initialList = []

        for _, row in enumerate(rowList):
            rowInitial= row.text.strip()[0]
            initialList.append(rowInitial)
            textRight = row.find('td',attrs={'text-right'}).text.strip()
            if rowInitial == "S":
                durations.append(textRight)
            elif rowInitial == "T":
                genres.append(textRight.replace("\n",", "))
        if len(initialList)!=2:
            if "S" not in initialList:
                durations.append("-")
            elif "T" not in initialList:
                genres.append("-")
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

        #test
        print(len(titles),len(releaseDates))
    tvseriesCount+=countPage
    print('Page %d/%d is done. %d/%d tvseries'%(page,pagesTvseries,countPage,tvseriesCount))
    sleep(randint(2,3))
    r = requests.get('https://www.sinefil.com/%s/tvseries/watched/%d'%(name,page))
    soup = BeautifulSoup(r.content,'lxml')
    tvseries_div = soup.find_all('div',attrs={'class':['movie','movie first']})




myMovies = pd.DataFrame({
'Type':types,
'Titles':titles,
'Duration':durations,
'Release Date':releaseDates,
'IMDB Score':imdbScores,
'Genre':genres,
'Image':images,})

totalCounts = pd.DataFrame({
    'tvSeriesCount':tvseriesCount})

myMovies.to_excel('movies.xlsx','Main')
totalCounts.to_excel('movies.xlsx','Totals')
