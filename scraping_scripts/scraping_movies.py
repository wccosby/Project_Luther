import re
from collections import defaultdict
import dateutil.parser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

###
###
### format:
### movie name: [domestic opening weekend, foreign gross total, budget, genre, date]
###
###

# testing for 1 page first
def parse_movie_page(url_list):

    # movie_dict = defaultdict(list)

    # list of lists where each sub-list represents a row, 1st row is the column headers
    movie_data = [['MOVIE_NAME','DOMESTIC_OPENING','FOREIGN_TOTAL','BUDGET','GENRE','RELEASE_DATE']]

    director_data = [['MOVIE_NAME','DIRECTOR']]
    writer_data = [['MOVIE_NAME','Writer']]
    actor_data = [['MOVIE_NAME','ACTOR']]
    producer_data = [['MOVIE_NAME','PRODUCER']]
    composer_data = [['MOVIE_NAME','COMPOSER']]


    for url in url_list:
        # print "Getting url response..."
        response = requests.get(url)
        # should probably check to make sure the response code is good to continue
        if response.status_code == 200:
            #'''get the page and soup reference'''#
            movie_page = response.text
            movie_soup = BeautifulSoup(movie_page)

            '''
            MOVIE NAME
            '''
            # these are returning as unicode, so coerce to a standard string
            try:
                movie_name = str(movie_soup.find_all('td')[2].find('b').get_text(strip=True))
            except:
                # SKIP DAT SHIIIIIIIIIITTTTTT
                continue

            '''
            Scraping for actor/writer/director/producer/composer information
            '''

            '''
            Director
            '''
            try:
                directors = movie_soup.findAll('a',href=re.compile("Director&id"))
                for person in directors:
                    director_data.append([movie_name,person.get_text(strip=True)])
            except:
                print "Couldn't find a director for: ", movie_name

            '''
            Writers
            '''
            try:
                writers = movie_soup.findAll('a',href=re.compile("Writer&id"))
                for person in writers:
                    writers_data.append([movie_name,person.get_text(strip=True)])
            except:
                print "Couldn't find a writer for: ", movie_name


            '''
            Actors
            '''
            try:
                actors = movie_soup.findAll('a',href=re.compile("Actor&id"))
                for person in actors:
                    actor_data.append([movie_name,person.get_text(strip=True)])
            except:
                print "Couldn't find actor for: ", movie_name

            '''
            Producers
            '''
            try:
                producers = movie_soup.findAll('a',href=re.compile("Producer&id"))
                for person in producers:
                    producer_data.append([movie_name,person.get_text(strip=True)])
            except:
                print "Couldn't find a writer for: ", movie_name


            '''
            Composers
            '''
            try:
                composers = movie_soup.findAll('a',href=re.compile("Composer&id"))
                for person in composers:
                    producer_data.append([movie_name,person.get_text(strip=True)])
            except:
                print "Couldn't find a writer for: ", movie_name



            '''
            DOMESTIC OPENING WEEKEND
            '''
            domestic_opening = 0
            # sometimes they have "limited release" stuff
            try:
                domestic_opening_string = movie_soup.find_all(class_='mp_box_content')[1].find('tr').find_all('td')[1].get_text(strip=True)
                domestic_opening = int(domestic_opening_string.replace('$','').replace(',',''))
                # print "domestic opening: ",domestic_opening
                # movie_dict[movie_name].append(int(domestic_opening))
            except:
                # limited release
                try:
                    limited_domestic_opening_string = movie_soup.find_all(class_='mp_box_content')[1].find_all('tr')[1].find('b').get_text(strip=True)
                    limited_domestic_opening = int(limited_domestic_opening_string.replace('$','').replace(',',''))

                    # expanded release
                    expanded_domestic_opening_string = movie_soup.find_all(class_='mp_box_content')[1].find_all('tr')[3].find_all('td')[1].get_text(strip=True)
                    expanded_domestic_opening = int(expanded_domestic_opening_string.replace('$','').replace(',',''))

                    # get the total
                    domestic_opening = limited_domestic_opening + expanded_domestic_opening
                    # movie_dict[movie_name].append(total_domestic_opening)
                except:
                    domestic_opening = 0
                    # print "THIS MOVIE DIDNT FUCKING WORK~~~~~~~~: ", movie_name




            '''
            FOREIGN GROSS TOTAL
            '''
            foreign_total = 0
            # have to check if it has a foreign release
            # if it doesnt have a foreign release then just put in 0
            try:
                ftg_string = movie_soup.find(text="Foreign:").find_parent("td").find_next_sibling("td").get_text(strip=True)
                ftg = ftg_string.replace('$','').replace(',','')
                foreign_total = int(ftg)
                # movie_dict[movie_name].append(int(ftg))
            except: # no foreign release data
                foreign_total = 0
                # movie_dict[movie_name].append(0)


            '''
            BUDGET
            '''
            budget = 0
            try:
                budget_string = movie_soup.find(text=re.compile('Production Budget:')).findNextSibling().get_text(strip=True)
                budget = budget_string.replace('$','').replace(',','')
                # split the string, use the 2nd index to determine scale (itll be like ['245','million'])
                # this means that there was a value for this field
                if len(budget.split()) > 1:
                    if budget.split()[1] == 'million':
                        budget = int(budget.split()[0])*1000000
                        # movie_dict[movie_name].append(int(budget.split()[0])*1000000)
                    elif budget.split()[1] == 'thousand':
                        budget = int(budget.split()[0])*1000
                        # movie_dict[movie_name].append(int(budget.split()[0])*1000)
                    else:
                        print "oh"
                else:
                    # movie_dict[movie_name].append(0)
                    budget = 0
            except:
                budget = 0

            '''
            GENRE
            '''
            try:
                genre_obj = movie_soup.find(text=re.compile('Genre:'))
                genre_parent = genre_obj.find_parent('td')
                genre_string = genre_parent.find('b').get_text(strip=True)
            except:
                genre_string = 'NONE'
            # print "genre: ",genre_string
            # movie_dict[movie_name].append(genre_string)


            '''
            DATE
            '''
            try:
                date = movie_soup.find(text=re.compile('Release Date:')).find_parent('td').find('a').get_text(strip=True)
                datetime_obj = dateutil.parser.parse(date)
            except:
                datetime_obj = None
            # print "date time: ", datetime_obj
            # movie_dict[movie_name].append(datetime_obj)
        print "Finished parsing ", movie_name
        movie_data.append([movie_name,domestic_opening,foreign_total,budget,genre_string,datetime_obj])

    return movie_data, director_data, writer_data, actor_data, producer_data, composer_data


'''
Compiles a list of urls on the yearly movies page
'''
def get_movie_urls(list_url):
    url_list = []
    for url in list_url:
        not_movie_index = len(url_list)
        # print "Getting url response..."
        response = requests.get(url)
        # should probably check to make sure the response code is good to continue
        # print "got response, now getting text..."
        #'''get the page and soup reference'''#
        list_page = response.text
        list_soup = BeautifulSoup(list_page)

        # the first row is the title of the columns

        list_table = list_soup.find("table",{"cellspacing":"1","cellpadding":"5"})
        url_prefix ='http://boxofficemojo.com'
        for row in list_table.find_all("tr"):
            try:
                url_suffix = row.find('a')['href']
                # print url_suffix
                url_list.append(url_prefix + url_suffix)
            except:
                continue
                # print "not a movie title"
        url_list.pop(not_movie_index) # the first element is not a movie title
    return url_list

movie_list_pages_2015_2016 = ['http://www.boxofficemojo.com/yearly/chart/?yr=2016&p=.htm',
                    'http://www.boxofficemojo.com/yearly/chart/?page=2&view=releasedate&view2=domestic&yr=2016&p=.htm',
                    'http://www.boxofficemojo.com/yearly/chart/?page=3&view=releasedate&view2=domestic&yr=2016&p=.htm',
                    'http://www.boxofficemojo.com/yearly/chart/?page=4&view=releasedate&view2=domestic&yr=2016&p=.htm',
                    'http://www.boxofficemojo.com/yearly/chart/?yr=2015&p=.htm',
                    'http://www.boxofficemojo.com/yearly/chart/?page=2&view=releasedate&view2=domestic&yr=2015&p=.htm',
                    'http://www.boxofficemojo.com/yearly/chart/?page=3&view=releasedate&view2=domestic&yr=2015&p=.htm',
                    'http://www.boxofficemojo.com/yearly/chart/?page=4&view=releasedate&view2=domestic&yr=2015&p=.htm',
                    'http://www.boxofficemojo.com/yearly/chart/?page=5&view=releasedate&view2=domestic&yr=2015&p=.htm',
                    'http://www.boxofficemojo.com/yearly/chart/?page=6&view=releasedate&view2=domestic&yr=2015&p=.htm',
                    'http://www.boxofficemojo.com/yearly/chart/?page=7&view=releasedate&view2=domestic&yr=2015&p=.htm']

movie_list_pages_2013_2014 = ['http://www.boxofficemojo.com/yearly/chart/?yr=2014&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=2&view=releasedate&view2=domestic&yr=2014&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=3&view=releasedate&view2=domestic&yr=2014&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=4&view=releasedate&view2=domestic&yr=2014&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=5&view=releasedate&view2=domestic&yr=2014&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=6&view=releasedate&view2=domestic&yr=2014&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=7&view=releasedate&view2=domestic&yr=2014&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=8&view=releasedate&view2=domestic&yr=2014&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?yr=2013&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=2&view=releasedate&view2=domestic&yr=2013&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=3&view=releasedate&view2=domestic&yr=2013&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=4&view=releasedate&view2=domestic&yr=2013&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=5&view=releasedate&view2=domestic&yr=2013&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=6&view=releasedate&view2=domestic&yr=2013&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=7&view=releasedate&view2=domestic&yr=2013&p=.htm']

movie_list_pages_2010_2012 = ['http://www.boxofficemojo.com/yearly/chart/?yr=2012&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=2&view=releasedate&view2=domestic&yr=2012&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=3&view=releasedate&view2=domestic&yr=2012&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=4&view=releasedate&view2=domestic&yr=2012&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=5&view=releasedate&view2=domestic&yr=2012&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=6&view=releasedate&view2=domestic&yr=2012&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=7&view=releasedate&view2=domestic&yr=2012&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?yr=2011&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=2&view=releasedate&view2=domestic&yr=2011&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=3&view=releasedate&view2=domestic&yr=2011&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=4&view=releasedate&view2=domestic&yr=2011&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=5&view=releasedate&view2=domestic&yr=2011&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=6&view=releasedate&view2=domestic&yr=2011&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=7&view=releasedate&view2=domestic&yr=2011&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?yr=2010&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=2&view=releasedate&view2=domestic&yr=2010&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=3&view=releasedate&view2=domestic&yr=2010&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=4&view=releasedate&view2=domestic&yr=2010&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=5&view=releasedate&view2=domestic&yr=2010&p=.htm',
                            'http://www.boxofficemojo.com/yearly/chart/?page=6&view=releasedate&view2=domestic&yr=2010&p=.htm',]

# movie_urls = get_movie_urls(movie_list_pages_2010_2012)
# movie_data_list = parse_movie_page(movie_urls)

def get_budget_imdb(url_list):
    for url in url_list:
        # print "Getting url response..."
        response = requests.get(url)
        # should probably check to make sure the response code is good to continue
        if response.status_code == 200:
            #'''get the page and soup reference'''#
            movie_page = response.text
            movie_soup = BeautifulSoup(movie_page)


            budget = 0
            try:
                reduced = movie_soup.find('div',{"id":"titleDetails"})
                budget_string = reduced.find_all(text=re.compile('\$'))[0].strip()
                budget = int(budget_string.replace('$','').replace(',',''))
                # split the string, use the 2nd index to determine scale (itll be like ['245','million'])
                # this means that there was a value for this field
            except:
                print "NOPE"
                budget = 0
            print budget

def get_budget_numbers(url_list):
    for url in url_list:
        # print "Getting url response..."
        response = requests.get(url)
        # should probably check to make sure the response code is good to continue
        if response.status_code == 200:
            #'''get the page and soup reference'''#
            movie_page = response.text
            movie_soup = BeautifulSoup(movie_page)


            budget = 0
            try:
                print movie_soup
                # reduced = movie_soup.find('div',{"id":"titleDetails"})
                # budget_string = reduced.find_all(text=re.compile('\$'))[0].strip()
                # budget = int(budget_string.replace('$','').replace(',',''))
                # split the string, use the 2nd index to determine scale (itll be like ['245','million'])
                # this means that there was a value for this field
            except:
                print "NOPE"
                budget = 0
            print budget

# get_budget_imdb(['http://www.imdb.com/title/tt1024648/?ref_=fn_al_tt_1'])
get_budget_numbers(['http://www.the-numbers.com/movie/Argo#tab=summary'])
# need to write to csv
# import csv
# print movie_data_list
# with open("movie_data_2010_2012.csv", "wb") as f:
#     writer = csv.writer(f)
#     writer.writerows(movie_data_list)
