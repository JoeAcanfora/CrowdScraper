__author__ = 'joeacanfora'

from pageScrape import scrape_this_page
from pageScrape import make_soup
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from pyvirtualdisplay import Display
from selenium.common.exceptions import NoSuchElementException

START_URL = 'https://www.kickstarter.com/discover/categories/technology'
kickstart_url = 'https://www.kickstarter.com'

def check_exists_by_text(driver, text):

    try:
        driver.find_element_by_link_text(text).click()
    except NoSuchElementException:
        return False
    return True


def main():
    print 'starting scrape all...'



    display = Display(visible=0, size=(800, 600))
    display.start()
    #selenium
    driver = webdriver.Chrome()
    driver.get(START_URL)
    driver.implicitly_wait(2) # This line will cause it to search for 60 seconds
    result = True
    print "clicking Load more"
    while result:
        result = check_exists_by_text(driver, "Load more")
        time.sleep(1.5)
        print 'loading more...'

    #Beautiful soup
    soup = make_soup(driver.page_source)
    allRawPages = soup.findAll('div', 'project-thumbnail')

    #tidy-up selenium
    driver.quit()
    display.stop() # ignore any output from this.

    count = 0
    for rawPage in allRawPages:
        side_soup = BeautifulSoup(str(rawPage), 'lxml')
        href = side_soup.find('a', href=True)['href']

        url = kickstart_url + href
        scrape_this_page(url)
        print str(count) + ': ' + url
        count = count + 1
        time.sleep(3)


if __name__ == '__main__':
    main()


