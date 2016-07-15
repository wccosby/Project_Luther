import re
from collections import defaultdict
import dateutil.parser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests



# movie_data = []
#
# # header = ['Year','Total Gross','Change','Tickets Sold','Change','# of movies','Total Screens',
# #           'Avg. Ticket Price','Avg. Cost','#1 Movie']
# movie_data = []
#
# # the first row is the title of the columns
# for row in movie_table[2].findAll("tr"):
#     movie_row = []
#     for i,cell in enumerate(row.findAll("td")):
# #         print cell
#         movie_row.append(cell.find(text=True))
#     movie_data.append(movie_row)
#
# header = movie_data.pop(0)
# movies_df = pd.DataFrame(movie_data,columns = header)
# # movies_df.dropna()

###
###
### format:
### movie name: [domestic opening weekend, foreign gross total, budget, genre, date]
###
###

# testing for 1 page first
def parse_movie_page(url_list):

    movie_dict = defaultdict(list)

    for url in url_list:

        print "Getting url response..."
        response = requests.get(url)
        # should probably check to make sure the response code is good to continue
        if response.status_code == 200:
            print "got response, now getting text..."
            #'''get the page and soup reference'''#
            movie_page = response.text
            movie_soup = BeautifulSoup(movie_page)

            print "Soup object loaded"
            # MOVIE NAME
            # these are returning as unicode, so coerce to a standard string
            movie_name = movie_soup.find_all('td')[2].find('b').get_text(strip=True)
            # print "movie name: ",movie_name

            #''' DOMESTIC TOTAL GROSS '''#
        #     # can do this the normal, easy way, also it is present for every movie
        #     dtg_string = movie_soup.find(text=re.compile('Domestic Total')) # finds the label
        #     # format the dtg
        # #     dtg = dtg_string.findNextSibling().text # grabs the next value, which is the dtg
        #     dtg = dtg_string.find_parent("td").find('b').get_text(strip=True)
        #     dtg = dtg.replace('$','').replace(',','')
        #     print "domestic total gross: ",dtg
        #     movie_dict[movie_name].append(int(dtg))


            #''' DOMESTIC OPENING WEEKEND '''#
            # sometimes they have "limited release" stuff
            try:
                domestic_opening_string = movie_soup.find_all(class_='mp_box_content')[1].find('tr').find_all('td')[1].get_text(strip=True)
                domestic_opening = domestic_opening_string.replace('$','').replace(',','')
                # print "domestic opening: ",domestic_opening
                movie_dict[movie_name].append(int(domestic_opening))
            except:
                # limited release
                limited_domestic_opening_string = movie_soup.find_all(class_='mp_box_content')[1].find_all('tr')[1].find('b').get_text(strip=True)
                limited_domestic_opening = int(limited_domestic_opening_string.replace('$','').replace(',',''))

                # expanded release
                expanded_domestic_opening_string = movie_soup.find_all(class_='mp_box_content')[1].find_all('tr')[3].find_all('td')[1].get_text(strip=True)
                expanded_domestic_opening = int(expanded_domestic_opening_string.replace('$','').replace(',',''))

                # get the total
                total_domestic_opening = limited_domestic_opening + expanded_domestic_opening
                movie_dict[movie_name].append(total_domestic_opening)



            #''' FOREIGN GROSS TOTAL '''#
            # have to check if it has a foreign release
            # if it doesnt have a foreign release then just put in 0
            try:
                ftg_string = movie_soup.find(text="Foreign:").find_parent("td").find_next_sibling("td").get_text(strip=True)
                ftg = ftg_string.replace('$','').replace(',','')
                # print "foreign gross total: ",ftg
                movie_dict[movie_name].append(int(ftg))
            except: # no foreign release data
                # print "No foreign release information"
                movie_dict[movie_name].append(0)
        #
        #
        #     #''' BUDGET '''#
            # try:
            budget_string = movie_soup.find(text=re.compile('Production Budget:')).findNextSibling().get_text(strip=True)
            budget = budget_string.replace('$','').replace(',','')
            # split the string, use the 2nd index to determine scale (itll be like ['245','million'])
            print budget
            # this means that there was a value for this field
            if len(budget.split()) > 1:
                if budget.split()[1] == 'million':
                    movie_dict[movie_name].append(int(budget.split()[0])*1000000)
                elif budge.split()[1] == 'thousand':
                    movie_dict[movie_name].append(int(budget.split()[0])*1000)
                else:
                    print('THE BUDGET WAS ',budget.split())
            else:
                movie_dict[movie_name].append(0)
            #     if budget.split()[1] == 'million':
            #         movie_dict[movie_name].append(int(budget.split()[0]*1000000))
            #     elif budge.split()[1] == 'thousand':
            #         movie_dict[movie_name].append(int(budget.split()[0]*1000))
            #     else:
            #         print('THE BUDGET WAS ',budget.split())
            # except:
            #     print("No budget for ",movie_name," with string: ",movie_soup.find(text=re.compile('Production Budget:')))
            #     movie_dict[movie_name].append(int(0))



            #''' GENRE '''#
            genre_obj = movie_soup.find(text=re.compile('Genre:'))
            genre_parent = genre_obj.find_parent('td')
            genre_string = genre_parent.find('b').get_text(strip=True)
            # print "genre: ",genre_string
            movie_dict[movie_name].append(genre_string)


            #''' DATE '''#
            date = movie_soup.find(text=re.compile('Release Date:')).find_parent('td').find('a').get_text(strip=True)
            datetime_obj = dateutil.parser.parse(date)
            # print "date time: ", datetime_obj
            movie_dict[movie_name].append(datetime_obj)

            print

    return movie_dict



url2 = ['http://www.boxofficemojo.com/movies/?id=pixar2015.htm',
       "http://www.boxofficemojo.com/movies/?id=marvel2016.htm"]
url3 = ['http://www.boxofficemojo.com/movies/?id=pixar2015.htm',
       "http://www.boxofficemojo.com/movies/?id=marvel2016.htm",
       "http://www.boxofficemojo.com/movies/?id=deadpool2016.htm",
       'http://www.boxofficemojo.com/movies/?id=hello,mynameisdoris.htm']
url_pool = ["http://www.boxofficemojo.com/movies/?id=deadpool2016.htm"]

url_lim_opening = ['http://www.boxofficemojo.com/movies/?id=hello,mynameisdoris.htm']


test_dict = parse_movie_page(url3)
print "returned dictionary:"
print
for key, val in test_dict.iteritems():
    print key,': ',val
    print
