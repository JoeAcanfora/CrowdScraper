__author__ = 'joeacanfora'

from pageScrape import scrape_this_page
from kickstarterAPI import KickAPIClass
import time

# Main driver - first calls kickstarter api to get a list of project urls for
# the technology category.  Then it takes each url and hands it over to
# a script that scrapes that page and inserts the information into a database.
def main():
    print 'starting scrape all...'


    api = KickAPIClass("joeaca04@gmail.com", "ksSomo5158*")
    projs = api.track_category()

    count = 0
    for p in projs:
        print "processing " + str(count) + ': ' + p
        scrape_this_page(p)
        count = count + 1
        time.sleep(3)


if __name__ == '__main__':
    main()


