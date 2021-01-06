#   Author: Christopher Gambrell
#   Date: 12/8/2020
#
#   Webscrapper for Google News. Saves the resulting HTML from a given google news search. JSON will be created if articles are found in the HTML. 
#   

import requests
import json
from bs4 import BeautifulSoup

def run_news(parse=False, write=False,**params):
    URL = 'https://www.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&as_q={query}&as_occt=any&as_drrb=b&as_mindate={month}%2F%{from_day}%2F{year}&as_maxdate={month}%2F{to_day}%2F{year}&tbs=cdr%3A1%2Ccd_min%3A3%2F1%2F13%2Ccd_max%3A3%2F2%2F13&as_nsrc=Gulf%20Times&authuser=0'
    response = requests.get(URL.format(**params))
    html = response.text
    return parse_news(html, params['query'])

def parse_news(html, term):
    news_list = {term: []}
    soup = BeautifulSoup(html, 'html.parser')
    desiredClass='ZINbbc xpd O9g5cc uUPGi'
    for tag in soup.find_all("div", {"class":"ZINbbc xpd O9g5cc uUPGi"}):
        news_data_object = {}
        try:
            news_data_object['title'] = tag.find_next('h3').string
            news_data_object['link'] = (str(tag.find_next('a')['href']).split('&')[0]).split('/url?q=')[1]
            news_list[term].append(news_data_object)
        except:
            print('There was an error while creating the news_data_object.')
    return news_list

