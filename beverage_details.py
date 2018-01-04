# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 17:44:06 2017
@author: Vasthav
"""

import requests
import re
from bs4 import BeautifulSoup

final_list = []

def get_html(web_pages):  
    possible_links = []
    for web_page in web_pages:
        page = requests.get(web_page)
        soup = BeautifulSoup(page.content, 'html.parser')
        html_text = soup.find_all('td')
        possible_links.append(html_text)
    return possible_links #all the html details

        
def get_brewery_list(html_text): 
    brewery_links = []
    for html_link in html_text:
        for brewery_detail in html_link:
            possible_links = brewery_detail.find_all('a', attrs={'href': re.compile("/beer/profile/")})
            for link in possible_links:
                brewery_links.append(str(link.get('href')))
    return brewery_links

def get_bevarage_details(html_text):
    for bevarage_detail in html_text:
        possible_links = bevarage_detail.find_all('a', attrs={'href': re.compile("/beer/profile/")})
        for link in possible_links:
                url = 'https://www.beeradvocate.com' + str(link.get('href'))
                bevarage_details(url)
                
                
def get_bevarage_url(brewery_links):
    for link in brewery_links:
        page = requests.get('https://www.beeradvocate.com' + link)
        soup = BeautifulSoup(page.content, 'html.parser')
        html_text = soup.find_all('td')
        get_bevarage_details(html_text)


def bevarage_details(bevarage_url):
    if bevarage_url == "" or bevarage_url == None:
        return
    else:
        if "show" not in bevarage_url:
            page = requests.get(bevarage_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            title_box = soup.find_all('div', attrs={'class': re.compile("titleBar")})
            title = title_box[0]
            beer_details = title.h1.text.split("|")
            beer_name = beer_details[0].strip()
            brewery_name = beer_details[1].strip()
            #print(beer_name)
            #print(brewery_name)
            #print(title.h1.text)
            score_box_text = soup.find_all('div', attrs={'id': re.compile("score_box")})
            score = score_box_text[0]
            rating = score.find('span', class_ = 'ba-ravg')
            #print(rating.text)
            rating_text = score.find_all('b')
            #print(rating_text[1].text)
            info_box_text = soup.find_all('div', attrs={'id': re.compile("info_box")})
            details = info_box_text[0]
            location = details.find_all('a', attrs={'href': re.compile("/place/directory")})
            style = details.find_all('a', attrs={'href': re.compile("/beer/style")})
            #print(location[0].text)
            #print(style[0].text)
            abv = get_abv(info_box_text[0])
            date = get_added_date(info_box_text[0])
            availability = get_availability(info_box_text[0])
            #print(abv)
            #print(date)
            #print(availability)
            add_in_csv_list(beer_name, brewery_name, rating.text, rating_text[1].text, location[0].text, style[0].text, abv, date, availability)

def add_in_csv_list(beer_name, brewery_name, score, rating, location, style, abv, date, availability):
    row = ""
    row =  brewery_name + "," + beer_name + "," + location + "," +  abv + "," + style + "," + score + "," + rating + "," + availability + "," + date + "\n"
    final_list.append(row)
        
def print_in_csv(final_list):
    #dic = {"John": "john@example.com", "Mary": "mary@example.com"} #dictionary
    download_dir = "beer_advocate.csv" #where you want the file to be downloaded to 
    file = open(download_dir, "w") 
    #"w" indicates that you're writing strings to the file
    columnTitleRow = "Brewery1, Beer Name, Brewed in (location), ABV (alcohol volume), Style, Score, Ratings, Availability, Added On\n"
    #print(columnTitleRow)
    #print(final_list)
    file.write(columnTitleRow)
    for row in final_list:
        file.write(row)    
    #row =  brewery_name + "," + beer_name + "," + location + "," +  abv + "," + style + "," + score + "," + rating + "," + availability + "," + date + "\n"
    file.close()        
        
def get_abv(info_box):
    abv_percentage = ""
    abv_boolean = False
    for string in info_box.strings:
        if abv_boolean:
            abv_percentage = string.strip()
            abv_boolean = False
        if "Alcohol by volume" in string:
            abv_boolean = True
    return abv_percentage        
                
def get_added_date(info_box):
    date = ""
    for string in info_box.strings:
        if "Added by" in string:
            date = string.split(" ")
    return date[4]  

def get_availability(info_box):
    bevarage_availability = ""
    availability = False
    for string in info_box.strings:
        if availability:
            bevarage_availability = string.strip()
            availability = False
        if "Availability" in string:
            availability = True    
    return bevarage_availability             


if __name__ == '__main__':
    #webpages = ["https://www.beeradvocate.com/place/list/?start=0&&brewery=Y&sort=name"]
    webpages = ["https://www.beeradvocate.com/place/list/?start=20&&brewery=Y&sort=name"]
    #for i in range(20,20,20):
        #webpages.append("https://www.beeradvocate.com/place/list/?start="+str(i)+"&&brewery=Y&sort=name")
    page_text = get_html(webpages) #web-links for breweries 
    
    brewery_links = get_brewery_list(page_text)
    beers = get_bevarage_url(brewery_links)
    bevarage_details(beers)
    print_in_csv(final_list)