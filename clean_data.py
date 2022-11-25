import pandas as pd
import zipfile
import os
import requests


def find_archive():
    for j in os.scandir('.'):
        if j.is_file():
            if j.name.endswith('.zip') and j.name.startswith('letterboxd-'):
                return j
            elif j.name == 'simple_data.zip':
                return j


def extract_info(df, api, is_year=True):
    films_count = len(df)
    rating = df.groupby('Rating')['Name'].nunique().to_dict()
    [rating.update({i / 2: 0}) for i in range(1, 11) if i / 2 not in rating]
    rating = dict(sorted(rating.items()))
    avg_rating = "{:.1f}".format(df['Rating'].mean())
    highest_rated, lowest_rated, api_data = None, None, []
    if films_count > 10:
        # top five best & worst films if there are more then 10 films
        keys = ['Name', 'Rating']
        if api: keys.append('Vote_average')
        highest_rated = df.nlargest(5, 'Rating')[keys].to_dict(orient='list')
        lowest_rated = df.nsmallest(5, 'Rating')[keys].to_dict(orient='list')
        if len(keys) == 3:
            highest_rated['Rating'] = [f"{highest_rated['Rating'][i]}  |  {highest_rated['Vote_average'][i] / 2:.1f}"
                                       for i in range(5)]
            lowest_rated['Rating'] = [f"{lowest_rated['Rating'][i]}  |  {lowest_rated['Vote_average'][i] / 2:.1f}"
                                      for i in range(5)]
    if is_year:
        # num films by month/year
        count_by_period = df.groupby(df['Date'].dt.month)['Name'].nunique().to_dict()
        [count_by_period.update({i: 0}) for i in range(1, 13) if i not in count_by_period]
        count_by_period = dict(sorted(count_by_period.items()))
    else:
        count_by_period = df.groupby(df['Date'].dt.year)['Name'].nunique().to_dict()
    if api:
        api_data.append(df[['Name', 'Genres']].explode('Genres').groupby('Genres')['Name'].nunique().to_dict())
        api_data.append(df[['Name', 'Country']].explode('Country').groupby('Country')['Name'].nunique().to_dict())
        api_data.append(df['Runtime'].sum())

    return films_count, rating, avg_rating, highest_rated, lowest_rated, count_by_period, api_data


def extract_api(watched_data, api_key):
    problems, watched_data[['Country', 'Genres', 'Runtime', 'Vote_average']] = 0, None
    for index, film in enumerate(watched_data['Name'].to_list()):
        # you need to request general info, find an id and only then get detailed info using id
        id = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={film}')
        if id.status_code == 200 and id.json()['results']:
            req = requests.get(f'https://api.themoviedb.org/3/movie/{id.json()["results"][0]["id"]}?api_key={api_key}')
            if req.status_code == 200:
                watched_data.at[index, 'Country'] = [country['name'].replace('United States of America', 'USA')
                                                     if country['name'] == 'United States of America' else
                                                     country['name'].replace('United Kingdom', 'UK')
                                                     for country in req.json()['production_countries']]
                watched_data.at[index, 'Genres'] = [genre['name'].replace('Science Fiction', 'Sci-Fi') for genre in
                                                    req.json()['genres']]
                watched_data.at[index, 'Runtime'] = req.json()['runtime']
                watched_data.at[index, 'Vote_average'] = req.json()['vote_average']
            else:
                # probably unstable connection
                problems += 1
        else:
            # probably not film
            problems += 1
    return watched_data, problems


def main(api=''):
    with zipfile.ZipFile(find_archive()) as zf:
        #####################################################################################
        # Some people (well, me at least) have separate lists for every year, since there is no way to tell
        # letterboxd that I've seen that movie as a child and just want to rate it without adding it to watched.
        # So if you like me change like_me to True and rewrite filter
        #####################################################################################
        like_me, filter = False, 'lists/20'
        if like_me:
            year_lists = [i for i in zf.namelist() if i.startswith(filter)]
            watched_by_year = pd.concat(pd.read_csv(zf.open(i))['Name'] for i in year_lists)
            watched_data = pd.merge(pd.read_csv(zf.open('watched.csv'))[['Name', 'Date']], watched_by_year, on='Name')
        else:
            watched_data = pd.read_csv(zf.open('watched.csv'))[['Name', 'Date']]

        watched_data = pd.merge(watched_data, pd.read_csv(zf.open('ratings.csv'))[['Name', 'Rating']], on='Name')
        rewies_data, comments_data = pd.read_csv(zf.open('reviews.csv')), pd.read_csv(zf.open('comments.csv'))

    # make Date column type actually a date type
    watched_data['Date'] = pd.to_datetime(watched_data['Date'])
    rewies_data['Date'] = pd.to_datetime(rewies_data['Date'])
    comments_data['Date'] = pd.to_datetime(comments_data['Date'])

    rewies_by_year = rewies_data.groupby(rewies_data['Date'].dt.year)['Name'].nunique().to_dict()
    comments_by_year = comments_data.groupby(comments_data['Date'].dt.year)['Comment'].nunique().to_dict()

    problems = 0
    if api:
        watched_data, problems = extract_api(watched_data, api)
    # make list of dataframes by splitting by year watched_data
    g = watched_data.groupby(pd.Grouper(key='Date', freq='Y'))
    yearly_data = [group for df, group in g]
    overall = extract_info(watched_data, api, False)
    films_by_year = dict.fromkeys(overall[5])
    [films_by_year.update({year: extract_info(yearly_data[i], api)}) for i, year in enumerate(films_by_year)]
    films_by_year['Overall'] = overall
    del yearly_data, watched_data
    return films_by_year, problems, comments_by_year, rewies_by_year
