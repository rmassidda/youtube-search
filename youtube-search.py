#!/usr/bin/python3
import urllib
import argparse
from bs4 import BeautifulSoup

def main(limit,query,title,all):
    #   Query
    baseurl = 'https://duckduckgo.com/lite/'
    prefix = 'site:youtube.com '

    # User agent
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}

    # Prepare for POST request
    data = urllib.parse.urlencode({'q': prefix+query})
    data = data.encode('ascii')
    request=urllib.request.Request(baseurl,data,headers)
    f = urllib.request.urlopen(request)

    #   Parsing
    soup = BeautifulSoup(f.read(),'html.parser')
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
        if ('watch' in href) or all:
            #   Print
            if(title):
                print(text)
            print(href)
            #   Increment counter
            counter = counter + 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Youtube CLI searcher')
    parser.add_argument('--notitle',help='print only urls',action='store_false')
    parser.add_argument('--all',help='include channels, playlists, etc.',action='store_true')
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

    main(limit,querystring,args.notitle,args.all)
