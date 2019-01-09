#!/usr/bin/python3
import requests
import argparse
from bs4 import BeautifulSoup

def main(limit,query,title,vonly):
    #   Query
    baseurl = 'https://duckduckgo.com/lite/'
    prefix = 'site:youtube.com '
    #   Post request to DDG <3
    r = requests.post(baseurl, data = {
        'q' : prefix+query
    })
    #   Parsing
    soup = BeautifulSoup(r.text,'html.parser')
    results = soup.find_all('a')
    #   Check if there are results
    if not results:
        print('No results!')
    #   Print results
    counter = 0
    for link in results:
        #   Check limit
        if(counter>=limit):
            break
        #   Data Getter
        text = link.get_text()
        href = link.get('href')
        if (vonly and 'watch' in href) or not vonly:
            #   Print
            if(title):
                print(text)
            print(href)
            #   Increment counter
            counter = counter + 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Youtube CLI searcher')
    parser.add_argument('--notitle',help='print only urls',action='store_false')
    parser.add_argument('--vonly',help='remove channels, playlists, etc.',action='store_true')
    parser.add_argument('-l',dest='limit',help='limits the number of results',action='store')
    parser.add_argument('query',help='search query',nargs='+')
    args = parser.parse_args()

    #   Limit the results
    try:
        limit = int(args.limit)
    except TypeError:
        limit = 5
    #   Create query
    querystring = ''
    for keyword in args.query:
        querystring = querystring + keyword + ' '

    main(limit,querystring,args.notitle,args.vonly)
