from bs4 import BeautifulSoup
import requests
import csv
from itertools import zip_longest
import pandas as pd
import numpy as np

# Here we declare the lists we will need during the web scraping. 
# Our goal is to scrape the best 100 movies titles,critical scores and number of critical rating.

movies_url = []
crit_score = []
titles = []
number_of_critic_ratings = []
audience_score = []
number_of_audience_ratings = []

# we use get method to get the page we want to scrape

result = requests.get("https://editorial.rottentomatoes.com/guide/best-movies-of-all-time/")

# We use content method to get the content of the page

src = result.content

# We use lxml parser to  make high-performance parsing and easy integration with other libraries
soup = BeautifulSoup(src, "lxml")

# This loop is for getting the urls for the movies that are in the main page of rottentomatoes
# <a> tag is for urls that's why we have included it in find_all method 

for movie in soup.find_all("a", {"class":"title"} ):
    movies_url.append(movie.get('href'))


movies_url = movies_url[:100]

# This loop for scraping the inner pages for each of the 100 url of the movies that we have stored in movies_url list
for url in movies_url:
    # This to get the content of each movie page 
    result2 = requests.get(url)
    src2 = result2.content
    soup2 = BeautifulSoup(src2, "lxml")

    # This is to get the title of the movie
    title = soup2.find("h1", {"class":"unset"}).text
    titles.append(title[1:-1])

    # This is to get the critical score of the movie
    score = soup2.find("rt-button", {"slot":"criticsScore"}).text
    score = score.strip()
    score=score[:-1]
    crit_score.append(score)

    #This is to get the number of critical reviews 
    crit_rate = soup2.find("rt-link", {"slot":"criticsReviews"}).text
    num=""
    for i in crit_rate:
        if i.isdigit():
            num+=i
    number_of_critic_ratings.append(num)

    # This is to get the audience score of the movie
    aud_score = soup2.find("rt-button",{"slot":"audienceScore"}).text
    aud_score = aud_score.strip()
    aud_score=aud_score[:-1]
    audience_score.append(aud_score)


    # This is to get the number of audience reviews
    aud_rate = soup2.find("rt-link", {"slot":"audienceReviews"}).text
    num2=""
    for i in aud_rate:
        if i.isdigit():
            num2+=i
    number_of_audience_ratings.append(num2)
    






# We use numpy to get a list of 100 in order to rank the movies 
ranking = np.arange(1,101)
ranking = list(ranking)

file_list = [ranking,crit_score,titles,number_of_critic_ratings,audience_score,number_of_audience_ratings]
exported = zip_longest(*file_list)

with open("bestofmovies.csv", "w" , newline='' ) as myfile:
    wr = csv.writer(myfile)
    wr.writerow(['ranking','critic_score', 'title', 'number_of_critic_ratings','audience_score','number_of_audience_ratings'])
    wr.writerows(exported)