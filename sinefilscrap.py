import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import numpy as np
from time import sleep
from random import randint
name = 'oorucelik'
r = requests.get('https://www.sinefil.com/%s/all/watched'%name)
soup = BeautifulSoup(r.content,'lxml')
movie_div = soup.find_all('div',attrs={'class':'col-lg-9'})
images_div = soup.find_all('div',attrs={'class':'col-lg-3'})
images = []
titles = []
durations = []
releaseDates = []
imdbScores = []
genres = []
#descriptions = []

pages = int(soup.find('div',attrs={'class':'pagination right'}).text[10:12])
print(pages)
for page in range(2,pages+1):

    for i,container in enumerate(movie_div) :

        #title
        title = container.h3.a.text
        titles.append(title)

        #releaseDate
        releaseDate = container.h3.span.text[2:-1]
        releaseDates.append(releaseDate)

        #duration
        durationTable = container.table.find_all('td',class_='text-right')
        if len(durationTable)==0:
            durations.append('-')
        else:
            for duration in durationTable:
                if len(durationTable)>1:
                    durations.append(durationTable[1].text.strip())
                    break
                else:
                    durations.append(duration.text.strip())

        #description
         #if container.p is not None:
           # descriptions.append(container.p.text)
           # else:
           # descriptions.append('-')\"\"\"

        #genres
        genreTable = container.table.find_all('a')
        if len(genreTable)==0:
            genres.append('-')
        else:
            for k, _ in enumerate(genreTable):
                if len(genreTable)==1:
                    genres.append(genreTable[k].text)
                elif len(genreTable)==2:
                    genres.append(genreTable[k].text+','+genreTable[k+1].text)
                    break
                else:
                    genres.append(genreTable[k].text+','+genreTable[k+1].text+','+genreTable[k+2].text)
                    break

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
    
 
    for i in images_div:
        images.append(i.img['data-src'])
    print('Page %d/%d is done'%(page,pages))
    sleep(randint(2,10))
    r = requests.get('https://www.sinefil.com/%s/all/watched/%d'%(name,page))
    soup = BeautifulSoup(r.content,'lxml')
    movie_div = soup.find_all('div',attrs={'class':'col-lg-9'})
    images_div = soup.find_all('div',attrs={'class':'col-lg-3'})

myMovies = pd.DataFrame({
'title':titles,
'duration':durations,
'releaseDate':releaseDates,
'IMDB':imdbScores,
'genre':genres,
'image':images})

#transform duration to hh:mm format
#hours = myMovies['duration'].str.extract('( .*(?= Saat))')
#minutes = myMovies['duration'].str.extract('( .*(?= Dk.))')
#hours = [hours[0][i].strip() if type(hours[0][i]) != float else hours[0][i] for i in range(len(hours[0]))]
#minutes = [minutes[0][i][-2:].strip() if type(minutes[0][i]) != float else minutes[0][i] for i in range(len(minutes[0]))]
#minutes = ['0'+str(i) if len(str(i))==1 else str(i) for i in minutes]
#myMovies['duration'] = [str(hours[i])+':'+str(minutes[i]) if type(hours[i]) != float else minutes[i] for i in range(len(hours)) ]

myMovies.to_excel('movies.xlsx')
