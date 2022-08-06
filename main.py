import pandas as pd
import zipfile
import os
import requests

def find_archive():
    for dirs, dir, files in os.walk('.'):
        for j in files:
            if j.endswith('utc.zip'): return j

def extract_info(df, api, isyear=1):
    films_count = len(df)
    rating = df.groupby('Rating')['Name'].nunique().to_dict()
    avg_rating = "{:.1f}".format(df['Rating'].mean())

    if films_count > 10:
        highest_rated = df.nlargest(5, 'Rating')[['Name', 'Rating']].to_dict(orient='records')
        lowest_rated = df.nsmallest(5, 'Rating')[['Name', 'Rating']].to_dict(orient='records')

    else:
        highest_rated, lowest_rated = None, None

    if isyear:
        count_by_period = df.groupby(df['Date'].dt.month)['Name'].nunique().to_dict()
    else:
        count_by_period = df.groupby(df['Date'].dt.year)['Name'].nunique().to_dict()

    api_data = []
    if api:
        countries = df[['Name', 'Country']].explode('Country').groupby('Country')['Name'].nunique().to_dict()
        genres = df[['Name', 'Genres']].explode('Genres').groupby('Genres')['Name'].nunique().to_dict()
        runtime = df['Runtime'].count()
        api_data = [countries, genres, runtime]

    return films_count, rating, avg_rating, highest_rated, lowest_rated, count_by_period, api_data

with zipfile.ZipFile(find_archive()) as zf:
    watched_data = pd.merge(pd.read_csv(zf.open('watched.csv'))[ ['Name', 'Date'] ],
                            pd.read_csv(zf.open('ratings.csv'))[ ['Name', 'Rating'] ],
                            on='Name')
    rewies_data = pd.read_csv(zf.open('reviews.csv'))
    comments_data = pd.read_csv(zf.open('comments.csv'))

watched_data['Date']= pd.to_datetime(watched_data['Date'])
rewies_data['Date']= pd.to_datetime(rewies_data['Date'])
comments_data['Date']= pd.to_datetime(comments_data['Date'])

rewies_by_year = rewies_data.groupby(rewies_data['Date'].dt.year)['Name'].nunique().to_dict()
comments_by_year = comments_data.groupby(comments_data['Date'].dt.year)['Comment'].nunique().to_dict()

api_key = 'e840a47026103ff8619463cb2716132d'
api = True

genres = []
countries = []
runtime = []
for film in watched_data['Name']:
    id = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + api_key +'&query=' + film)
    if id.status_code == 200 and id.json()['results']:
        req = requests.get('https://api.themoviedb.org/3/movie/' + str(id.json()['results'][0]['id']) + '?api_key=' + api_key)
        if req.status_code == 200:
            countries.append([country['name'] for country in req.json()['production_countries']])
            genres.append([genre['name'] for genre in req.json()['genres']])
            runtime.append(req.json()['runtime'])
        else:
            print(req.status_code, req.json(), watched_data.index[watched_data['Name'] == film].to_list())
    else:
        print(id.status_code, id.json(), watched_data.index[watched_data['Name'] == film].to_list())

watched_data['Country'] = countries
watched_data['Genres'] = genres
watched_data['Runtime'] = runtime

g = watched_data.groupby(pd.Grouper(key='Date', freq='Y'))
yearly_data = [group for df,group in g]

e = extract_info(watched_data, api, None)
for i in e: print(i)
for i in yearly_data: print(extract_info(i, api))
