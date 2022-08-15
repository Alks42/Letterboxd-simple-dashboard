#####################################################################################
# This file basically for peaople like me who created lists with films that they'd wached long
# time ago. But since there is no way to tell that to letterboxd these people
# (well, me at least) also created lists for each year. To use it just put
# import alternative_clean_data as clean_data instead of import clean_data
# and rewrite filter.
#####################################################################################
import pandas as pd
import zipfile
import os
import requests

def find_archive():
    for dirs, dir, files in os.walk('.'):
        for j in files:
            if j.endswith('.zip') and j.startswith('letterboxd-'): return j
            elif j == 'simple_data.zip': return j

def extract_info(df, api, isyear=1):
    films_count = len(df)
    rating = df.groupby('Rating')['Name'].nunique().to_dict()
    for i in range(1,11):
        if i/2 not in rating: rating[i/2] = 0
    rating = dict(sorted(rating.items()))
    avg_rating = "{:.1f}".format(df['Rating'].mean())

    if films_count > 10:
        # top five best & worst films if there are more then 10 films
        keys = ['Name', 'Rating']
        if api: keys.append('Vote_average')
        highest_rated = df.nlargest(5, 'Rating')[keys].to_dict(orient='list')
        lowest_rated = df.nsmallest(5, 'Rating')[keys].to_dict(orient='list')
        if len(keys) == 3:
            for i in range(5):
                highest_rated['Rating'][i] = str(highest_rated['Rating'][i]) + '   |   ' + '{:.1f}'.format(highest_rated['Vote_average'][i]/2)
            for i in range(5):
                lowest_rated['Rating'][i] = str(lowest_rated['Rating'][i]) + '   |   ' + '{:.1f}'.format(lowest_rated['Vote_average'][i]/2)

    else:
        highest_rated, lowest_rated = None, None

    if isyear:
        # num films by month/year
        count_by_period = df.groupby(df['Date'].dt.month)['Name'].nunique().to_dict()
        for i in range(1, 13):
            if i not in count_by_period: count_by_period[i] = 0
        count_by_period = dict(sorted(count_by_period.items()))
    else:
        count_by_period = df.groupby(df['Date'].dt.year)['Name'].nunique().to_dict()

    api_data = []
    if api:
        api_data.append(df[['Name', 'Genres']].explode('Genres').groupby('Genres')['Name'].nunique().to_dict())
        api_data.append(df[['Name', 'Country']].explode('Country').groupby('Country')['Name'].nunique().to_dict())
        api_data.append(df['Runtime'].sum())
        # [geners, countries, runtime]

    return films_count, rating, avg_rating, highest_rated, lowest_rated, count_by_period, api_data

def main(api=''):

    def run_api(api_key):
        nonlocal watched_data, problems
        watched_data[['Country', 'Genres', 'Runtime', 'Vote_average']] = None
        index = 0
        for film in watched_data['Name'].to_list():
            # looks a bit stupid, but you really need to request general info
            # find an id and only then get detailed info with id
            id = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + api_key + '&query=' + film)
            if id.status_code == 200 and id.json()['results']:
                req = requests.get(
                    'https://api.themoviedb.org/3/movie/' + str(id.json()['results'][0]['id']) + '?api_key=' + api_key)
                if req.status_code == 200:
                    watched_data.at[index, 'Country'] = [country['name'].replace('United States of America', 'USA')
                                                         if  country['name'] == 'United States of America' else
                                                         country['name'].replace('United Kingdom', 'UK')
                                                         for country in req.json()['production_countries']]
                    watched_data.at[index, 'Genres'] = [genre['name'].replace('Science Fiction', 'Sci-Fi') for genre in req.json()['genres']]
                    watched_data.at[index, 'Runtime'] = req.json()['runtime']
                    watched_data.at[index, 'Vote_average'] = req.json()['vote_average']
                else:
                    # probably internet conection
                    problems += 1
                    # print(req.status_code, req.json(), watched_data.index[watched_data['Name'] == film].to_list())
            else:
                # probably tv series or so
                problems += 1
                # print(id.status_code, id.json(), watched_data.index[watched_data['Name'] == film].to_list())
            index += 1

    with zipfile.ZipFile(find_archive()) as zf:
        ############################### different part ##################################
        year_lists = []
        for i in zf.namelist(): # filter
            if i.startswith('lists/20'): year_lists.append(i)

        wached_data_by_year = pd.concat(pd.read_csv(zf.open(i))['Name'] for i in year_lists)
        watched_data = pd.merge(pd.read_csv(zf.open('watched.csv'))[ ['Name', 'Date'] ],
                                wached_data_by_year, on='Name')
        #####################################################################################
        watched_data = pd.merge(watched_data,
                                pd.read_csv(zf.open('ratings.csv'))[ ['Name', 'Rating'] ],
                                on='Name')
        rewies_data = pd.read_csv(zf.open('reviews.csv'))
        comments_data = pd.read_csv(zf.open('comments.csv'))

    # make Date column type actually a date type
    watched_data['Date']= pd.to_datetime(watched_data['Date'])
    rewies_data['Date']= pd.to_datetime(rewies_data['Date'])
    comments_data['Date']= pd.to_datetime(comments_data['Date'])

    rewies_by_year = rewies_data.groupby(rewies_data['Date'].dt.year)['Name'].nunique().to_dict()
    comments_by_year = comments_data.groupby(comments_data['Date'].dt.year)['Comment'].nunique().to_dict()

    problems = 0
    if api: run_api(api)

    # make list of dfs by spliting by year wached_data
    g = watched_data.groupby(pd.Grouper(key='Date', freq='Y'))
    yearly_data = [group for df,group in g]

    overall = extract_info(watched_data, api, None)
    films_by_year = dict.fromkeys(overall[5])
    j = 0
    for i in films_by_year.keys():
        films_by_year[i] = extract_info(yearly_data[j], api)
        j += 1
    films_by_year['Overall'] = overall
    del yearly_data, watched_data
    return films_by_year, problems, comments_by_year, rewies_by_year