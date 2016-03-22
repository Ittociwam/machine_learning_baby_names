import os
import csv
import tmdbsimple as tmdb
import json
import requests



# start_year = 1940
# this_year = 2016
#
# func(x, y)
#
# for year from start year to this_year
#   actors = []
#   character_names = []
#   top_x_movies[] = top x movies from year
#   for movie in top_x_movies
#     actors += movie.actors
#     character_names += movie.char_names
#
#   for name in actors, character_names
#     for year in range(y)(ex. year-5 to year+5)
# 	for file_name in files
# 		if file_name has year
# 			for baby_names in file
# 				is baby_name in name

year = 2005
x = 0
# Read in the csv and put the names and their counts for that year into a dict
for i_year in (range(year - x, year + (x+ 1))):
    path = os.getcwd()
    file_path = path + '/names/yob' + str(i_year) + '.csv'
    if os.path.exists(file_path):
        print("found", i_year, "file")
        file = open(file_path, 'r')
        names = csv.reader(file)
        baby_names = {}
        for i, name in enumerate(names):
            baby_names[name[0]]= name[2]
            print(name)




tmdb.API_KEY = 'e026cff454ca0e6e446e959e87c05bcf'



# Get the  top movies for a year (10 per page)
kwargs = {'primary_release_year':'2010', 'page':'2'}
disc_obj = tmdb.Discover()
top = disc_obj.movie(**kwargs)
movies = top['results']
movie_ids = []
for item in movies:
    movie_ids.append(item['id'])
for id in movie_ids:
    print(id)

# get the names of cast and characters
names_list = []
movie = tmdb.Movies(603)
response = movie.info()
print(movie.title)
cast = movie.credits()['cast']
for value in cast:
    names_list.append(value['character'])
    names_list.append(value['name'])
    print (value['character'], '-', value['name'])

# Store the names and num of babies born with that name for every name that showed up in the movie
names_dict = {}
for baby_name in baby_names:
    if baby_name in names_list:
        try:
            names_dict[baby_name] = names_dict[baby_name] + baby_names[baby_name]
        except KeyError:
            names_dict[baby_name] = baby_names[baby_name]
for i in names_dict.items():
    print (i)