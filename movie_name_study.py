import os
import csv
import tmdbsimple as tmdb
import re
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import datetime
from matplotlib.dates import YearLocator



class MovieNameStudy:

    def __init__(self, year, span, pages=1):
        print("Passed in ", year, span)
        tmdb.API_KEY = 'e026cff454ca0e6e446e959e87c05bcf'
        self.year = int(year)
        self.span = int(float(span))
        self.pages = int(pages)
        self.name_results = {}
        self.get_names()


        self.get_cast_names()
        for i in self.name_results:
            if self.name_results[i].movies:
                print(i)
                pprint(self.name_results[i].occurrences)
                print("Movies containing", i, '\n', self.name_results[i].movies, "\n")
                display = self.name_results[i]


        #for data_dict in display.occurrences:
        x = []
        y = []
        for key, value in display.occurrences.items():
            x.append(int(key))
            y.append(int(value))
        #plt.xticks()
        print("x: ", x, "y: ", y)
        plt.scatter(x, y)
        plt.title(display.name + ' - ' + str(display.movies))
        print(min(x), max(x))
        ax = plt.gca()
        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        plt.draw()
        #plt.axis([min(x), max(x), min(y), max(y)])
        plt.xlabel("Year")
        plt.ylabel("Occurrences")
        #plt.legend(display.occurrences.keys())
        plt.show()
    class Name:
        def __init__(self, name, year, num):
            self.name = name
            self.occurrences = {year: num}
            self.movies = {}

        def add_year(self, add_year, num):
            if add_year in self.occurrences:
                self.occurrences[add_year] = int(self.occurrences[add_year]) + int(num)
            else:
                self.occurrences[add_year] = num


    def count_instances(self, movie_name, names_list):
        # Store the names and num of babies born with that name for every name that showed up in the movie
        names_dict = {}
        for name in names_list:
            try:
                self.name_results[name].movies[movie_name] = self.year
            except KeyError:
                print(name, "not used")

    # Read in the csv and put the names and their counts for that year into a dict
    def get_names(self):
        for i_year in (range(self.year - self.span, self.year + (self.span+ 1))):
            path = os.getcwd()
            file_path = path + '/names/yob' + str(i_year) + '.csv'
            if os.path.exists(file_path):
                print("found", i_year, "file")
                file = open(file_path, 'r')
                names = csv.reader(file)
                for i, name in enumerate(names):
                    if name[0] in self.name_results:
                        self.name_results[name[0]].add_year(i_year, name[2])
                    else:
                        self.name_results[name[0]] = self.Name(name[0], i_year, name[2])
                    #print(name)



    def has_numbers(self, input):
        return bool(re.search(r'\d', input))


    def get_cast_names(self):
        # Get the top movies for a year (10 per page)
        kwargs = {'primary_release_year':self.year, 'page':'1'}
        disc_obj = tmdb.Discover()
        top = disc_obj.movie(**kwargs)
        movies = top['results']
        movie_ids = []
        for item in movies:
            movie_ids.append(item['id'])
        for id in movie_ids:
            movie = tmdb.Movies(id)
            response = movie.info()
            print(movie.title)
            cast = movie.credits()['cast']
            names_list = []
            for value in cast:
                if not self.has_numbers(value['character']):
                    for n in value['character'].split(' '):
                        if n == '(voice)' or n is '/' or n is '|':
                            continue
                        names_list.append(n)
                for n in value['name'].split(' '):
                    names_list.append(n)
            print(names_list)
            self.count_instances(movie.title, names_list)



MovieNameStudy(1990, 3, 3)