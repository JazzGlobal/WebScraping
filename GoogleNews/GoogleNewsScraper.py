#   Author: Christopher Gambrell
#   Date: 12/8/2020
#
#   Webscrapper for Google News. Saves the resulting HTML from a given google news search. JSON will be created if articles are found in the HTML. 
#   
#   Example Usage #1
#   run_news(False,True,query="AMD", month=12, from_day=7, to_day=8, year=20)

#   Output: Generates resulting HTML from the search and saves it to a file. A JSON file with the following data will be saved. (Output will vary across date ranges.): 
#   [{"term": "AMD", "results": [{"title": "AMD Radeon RX 6900 XT review roundup: a niche purchase", "link": "https://www.theverge.com/22163537/amd-radeon-rx-6900-xt-review-roundup"}, {"title": "AMD's Radeon RX 6900 XT Graphics Cards Immediately Sell Out", "link": "https://www.pcmag.com/news/amds-radeon-rx-6900-xt-graphics-cards-immediately-sell-out"}, {"title": "Why AMD and NVIDIA Are Top Growth Stocks to Buy Right Now", "link": "https://www.fool.com/investing/2020/12/08/why-amd-nvidia-top-growth-stocks-buy-right-now/"}, {"title": "Lisa Su's Channel Awakening: Why Partners Could Be AMD's 'Largest Growth Opportunity'", "link": "https://www.crn.com/news/components-peripherals/lisa-su-s-channel-awakening-why-partners-could-be-amd-s-largest-growth-opportunity-"}, {"title": "Where to buy an AMD RX 6900 XT - live updates", "link": "https://www.pcgamer.com/news/live/where-to-buy-amd-rx-6900-xt/"}, {"title": "Apple Developing 32-Core ARM CPUs and 128-Core GPUs to Replace AMD Graphics, Report", "link": "https://www.tomshardware.com/news/apple-developing-32-core-arm-cpus-and-128-core-gpus-to-replace-amd-graphics-report"}, {"title": "Radeon 6900 XT Release Time and Best Tips for Ordering One", "link": "https://www.newsweek.com/radeon-6900-xt-release-time-best-tips-order-one-1552610"}, {"title": "AMD RX 6000 And NVIDIA RTX 30 Series GPUs Hit By Another Supply Constraint: GDDR6 Memory Shortage", "link": "https://wccftech.com/amd-rx-6000-and-nvidia-rtx-30-series-hit-by-another-supply-constraint-gddr6-memory-shortage/"}, {"title": "AMD, Nvidia Shortages Also Hurting System Builders", "link": "https://www.tomshardware.com/news/pre-builts-struggle-CPU-GPU-shortage"}, {"title": "Cyberpunk 2077 Could Be The Crysis of This Decade, Early PC Performance Benchmarks Show AMD Radeon & NVIDIA GeForce GPU Struggling at 4K Even Without Raytracing Enabled", "link": "https://wccftech.com/cyberpunk-2077-crysis-of-this-decade-pc-performance-benchmarks-nvidia-amd-gpus-dlss-raytracing/"}]}]

#   Example Usage #2
#   run_news(True,False,query="AMD", month=12, from_day=7, to_day=8, year=20)

#   Output: Generates resulting HTML from the search and saves it to a file. Returns the parsed data for custom processing. No JSON files are generated.


import requests
import json
from bs4 import BeautifulSoup


def run_news(parse=False, write=False,**params):
    URL = 'https://www.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&as_q={query}&as_occt=any&as_drrb=b&as_mindate={month}%2F%{from_day}%2F{year}&as_maxdate={month}%2F{to_day}%2F{year}&tbs=cdr%3A1%2Ccd_min%3A3%2F1%2F13%2Ccd_max%3A3%2F2%2F13&as_nsrc=Gulf%20Times&authuser=0'
    response = requests.get(URL.format(**params))
    print(response.url)
    print('Request Finished With Response Code:', response.status_code)
    title = params['query'] + str(params['month']) + str(params['from_day']) + str(params['to_day']) + str(params['year']) + "_webpage"
    f = open(f'{title}.html', 'w')
    f.write(response.text)
    f.close()
    if(parse):
        f = open(f'{title}.html', 'r')
        html = f.read()
        f.close()
        return parse_news(html)
    elif(write):
        f = open(f'{title}.html', 'r')
        html = f.read()
        f.close()
        data = parse_news(html)
        write_data(title, data, params['query'])

def parse_news(html):
    news_list = []
    soup = BeautifulSoup(html, 'html.parser')
    desiredClass='ZINbbc xpd O9g5cc uUPGi'
    for tag in soup.find_all("div", {"class":"ZINbbc xpd O9g5cc uUPGi"}):
        news_data_object = {}
        try:
            news_data_object['title'] = tag.find_next('h3').string
            news_data_object['link'] = (str(tag.find_next('a')['href']).split('&')[0]).split('/url?q=')[1]
            news_list.append(news_data_object)
        except:
            print('There was an error while creating the news_data_object.')
    return news_list

def write_data(filename, data, term=None):
    search_object = {'term': term, 'results': data}
    if(data):
        with open(f'{filename}.json', 'w') as fp:
            print('Dumping data to JSON')
            json.dump(search_object, fp)
