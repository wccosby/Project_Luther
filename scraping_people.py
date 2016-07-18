import re
from collections import defaultdict
import dateutil.parser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

def scrape_people(url_list):
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
    return director_data,writer_data,actor_data,producer_data,composer_data


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


movie_urls = get_movie_urls(movie_list_pages_2015_2016+movie_list_pages_2013_2014+movie_list_pages_2010_2012)
director_data, writer_data, actor_data, producer_data, composer_data = scrape_people(movie_urls)


# need to write to csv
import csv
with open("director_data.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(director_data)

with open("writer_data.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(writer_data)

with open("actor_data.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(actor_data)

with open("producer_data.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(producer_data)

with open("composer_data.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(composer_data)
