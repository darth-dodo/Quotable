import requests
from bs4 import BeautifulSoup


def quote_spider(imdb_id):
    '''Quotes for a particular Imdb ID'''
    url = "http://www.imdb.com/title/" + imdb_id + "/quotes"

    '''Goofs quotes for a particular Imdb ID'''
        # url = "http://www.imdb.com/title/" + imdb_id + "/goofs"

    '''Trivia for a particular Imdb ID'''
        # url = "http://www.imdb.com/title/" + imdb_id + "/trivia"

    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    quotes_list = []
    for quote in soup.findAll('div', {'class': 'sodatext'}):
        # print (quote.text).encode('utf-8')
        quotes_list.append((quote.text).encode('utf-8', errors="ignore"))
    return quotes_list


if __name__ == '__main__':
    ids = [
    'tt0468569',
           'tt0468569', 'tt0081846',
                  'tt0460649', 'tt0407887', 'tt0208092'
           ]

    for i, num in enumerate(ids):
        quotes = quote_spider(ids[i])
        print len(quotes)
        # for i, enum in enumerate(quotes):
            # print quotes[i]
        print '~' * 100
