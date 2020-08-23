import lxml
import requests
from bs4 import BeautifulSoup


class IMDBScraper(object):

    def __init__(self, url):
        page = requests.get(url)
        self.baseURL = 'https://www.imdb.com'
        self.soup = BeautifulSoup(page.content, 'lxml')

    def start(self):
        table = self.soup.find('table', {'class': 'chart'})
        rows = table.find_all('tr')
        # Remove table headers
        rows.pop(0)
        movies = []
        for row in rows:
            movie = {}
            cells = row.find_all('td')
            element = cells[1].find('a')
            movie['name'] = element.text.strip()
            people = element['title'].split(',')
            people = list(map(str.strip, people))
            movie['director'] = ' '.join(people[0].split(' ')[:-1])
            movie['stars'] = people[1:]
            movie['link'] = self.baseURL+element['href']
            movie['year'] = int(cells[1].find(
                'span', {'class': 'secondaryInfo'}).text.strip('()'))
            element = cells[2].find('strong')
            movie['rating'] = float(element.text.strip())
            movie['numRatings'] = int(
                element['title'].split(' ')[3].replace(',', ''))
            movies.append(movie)
        return movies


if __name__ == "__main__":
    scraper = IMDBScraper('https://www.imdb.com/chart/top/')
    scraper.start()
