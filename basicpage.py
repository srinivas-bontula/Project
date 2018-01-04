# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 17:44:06 2017
@author: Vasthav
"""

import csv
import requests
import re
from bs4 import BeautifulSoup

def get_html(web_pages):  
    possible_links = []
    for web_page in web_pages:
        page = requests.get(web_page)
        soup = BeautifulSoup(page.content, 'html.parser')
        html_text = soup.find_all('td')
        possible_links.append(html_text)
    return possible_links #all the html details

        #for text in h6:
            #print(text.get_text())
        #print(soup.prettify())
        
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
                print_in_csv(url)
                
                
def get_bevarage_url(brewery_links):
    for link in brewery_links:
        page = requests.get('https://www.beeradvocate.com' + link)
        soup = BeautifulSoup(page.content, 'html.parser')
        html_text = soup.find_all('td')
        get_bevarage_details(html_text)


def print_in_csv(bevarage_url):
    if "show" not in bevarage_url:
        print(bevarage_url)
        page = requests.get(bevarage_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        score_box_text = soup.find_all('div', attrs={'id': re.compile("score_box")})
        info_box_text = soup.find_all('div', attrs={'id': re.compile("info_box")})
        return 
        

'''def print_in_csv(final_text):
    outfile = open("draft_1.csv",'w')
    writer = csv.writer(outfile)
    for brewery in final_text:   
        for brewery_detail in brewery:    
            writer.writerow(brewery_detail.get_text())
    outfile.close()
'''    
if __name__ == '__main__':
    webpages = ["https://www.beeradvocate.com/place/list/?start=0&&brewery=Y&sort=name"]
    for i in range(20,100,20):
        webpages.append("https://www.beeradvocate.com/place/list/?start="+str(i)+"&&brewery=Y&sort=name")
    page_text = get_html(webpages) #web-links for breweries 
    brewery_links = get_brewery_list(page_text)
    beers = get_bevarage_url(brewery_links)
    print_in_csv(beers)
    

    #print(breweries)
    #beers = getBeers(breweries)
    #printInCSV(finalText)