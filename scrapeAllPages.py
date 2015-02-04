__author__ = 'joeacanfora'

from pageScrape import scrape_this_page
from pageScrape import make_soup
from bs4 import BeautifulSoup

START_URL = 'http://www.kickspy.com/projects/find?Keyboards=&Status=0&Settings.ExpandCategories=true&C=12&C=130&C=49&SortBy1'
kickstart_url = 'https://www.kickstarter.com'


def getHref(string):
    href_to_end = str(string).split('href="')[1]
    return href_to_end.split('">')[0]

def main():
    print 'starting scrape all...'
    soup = make_soup(START_URL)
    allRawPages = soup.findAll('div', 'project-box-description')
    # print allRawPages
    for rawPage in allRawPages:

        side_soup = BeautifulSoup(str(rawPage), 'lxml')
        raw_page_url = side_soup.find('a', href=True)

        href = getHref(raw_page_url)

        url = kickstart_url + href

        scrape_this_page(url)

if __name__ == '__main__':
    main()


