from bs4 import BeautifulSoup
from urllib2 import urlopen
import time
import csv
import os
import datetime

BASE_URL = "https://www.kickstarter.com/projects/1678731377/the-main-drain-attachable-urinal"

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def removeHtml(string):
    result = BeautifulSoup(string).findAll(text=True)
    strResult = str(result.__str__())
    strResult = strResult.strip("[u'")
    strResult = strResult.strip("']")
    strResult = strResult.strip("\n")
    strResult = strResult.strip("u'")
    return strResult

class KickstarterAuthor:

    full_name = None
    location = None
    bio = None
    website = None
    photoPresent = None
    verified = None
    project_id = None

    def __init__(self, url, project_id):

        authorSoup = make_soup(url)
        self.project_id = project_id
        self.full_name = removeHtml(str(authorSoup.find('span', 'identity_name')))
        self.location = removeHtml(str(authorSoup.find('p', 'h5 bold mb0')))
        self.bio = removeHtml(str(authorSoup.find('div', 'readability')))
        self.website = str(authorSoup.find('ul', 'links list h5 bold', href=True))

        self.write_author_csv()

    def write_author_csv(self):
        exists = os.path.exists('author_TABLE.csv')
        with open('author_TABLE.csv', 'a') as csvfile:

            colHeaders = ['project_id', 'full_name', 'location',
                          'bio', 'website', 'contact_info',
                          'photoPresent', 'verified']
            writer = csv.DictWriter(csvfile, fieldnames=colHeaders)

            if not exists:
                writer.writeheader()

            writer.writerow({'project_id': str(self.project_id), \
                             'full_name': str(self.full_name), \
                             'location': str(self.location), \
                             'bio': str(self.bio), \
                             'website': str(self.website)})
                             # 'contact_info': str(self.contactInfo), \
                             # 'verified': str(self.verified)})

class KickstarterReward:

    amount = None
    limited = None
    maxBackers = None
    numBackers = None
    deliveryDate = None
    shipsTo = None
    description = None
    project_id = None
    limited = False

    def __init__(self, amount, numBackers, dDate, description, project_id, maxBackers):

        self.amount = amount
        self.numBackers = numBackers
        self.deliveryDate = dDate
        # self.shipsTo = shipsTo
        self.description = description
        self.project_id = project_id
        self.maxBackers = maxBackers
        if self.maxBackers > 0:
            limited = True

        self.save_to_csv()

    def save_to_csv(self):
        exists = os.path.exists('rewards_TABLE.csv')
        with open('rewards_TABLE.csv', 'a') as csvfile:

            colHeaders = ['project_id', 'pledge_amount', 'num_backers',
                          'delivery_date', 'description', 'max_backers',
                          'limited']
            writer = csv.DictWriter(csvfile, fieldnames=colHeaders)

            if not exists:
                writer.writeheader()

            writer.writerow({'project_id': str(self.project_id), \
                             'pledge_amount': str(self.amount), \
                             'num_backers': str(self.numBackers), \
                             'delivery_date': str(self.deliveryDate), \
                             'description': str(self.description), \
                             'max_backers': str(self.maxBackers), \
                             'limited': str(self.limited)})


class KicktstarterPage:
    #private memebrs
    soup = None
    pageurl = None
    project_id = None
    urlExtension = None
    project_name = None
    date = None
    project_author = None
    numBackers = None
    pledged = None
    rawEndTime = None
    end_date = None
    location = None
    category = None
    mainVideoLink = None
    goal = None
    rewards = None
    updates = None
    comments = None
    faq = None
    author_code = None
    description = None
    risks = None

    #methods
    def __init__(self, url):
        self.soup = make_soup(url)
        self.pageurl = url

    def parseRewards(self):
        rewardList = []
        rawRewards = self.soup.findAll("li", "NS-projects-reward bg-grey-light rounded clip mb2 relative")
        for rawR in rawRewards:

            sideSoup = BeautifulSoup(str(rawR), "lxml")
            dirtyReward = sideSoup.find('div', 'NS_backer_rewards__reward p2')

            rewardSoup = BeautifulSoup(str(dirtyReward))
            pledgeAmount = removeHtml(str(rewardSoup.find('h5', 'mb1')))
            maxBackers = removeHtml(str(rewardSoup.find('p', 'backers-limits')))
            description = removeHtml(str(rewardSoup.find('div', 'desc h5 mb2 break-word')))
            delivery = removeHtml(str(rewardSoup.find('time', 'js-adjust-time')))
            numBackers = removeHtml(str(rewardSoup.find('span', 'num-backers mr1')))

            cleanReward = KickstarterReward(pledgeAmount, numBackers, delivery, description, self.project_id, maxBackers)

            rewardList.append(cleanReward)
        return rewardList

    def parsePage(self):
        self.project_id = BASE_URL.split('/')[4]
        urlExtension = BASE_URL.replace('https://www.kickstarter.com' , '')
        self.project_name = removeHtml(str(self.soup.find('a', href=urlExtension)))
        self.date = time.strftime("%d/%m/%Y")
        self.project_author = removeHtml(str(self.soup.find('a', href=urlExtension + '/creator_bio')))
        self.numBackers = removeHtml(str(self.soup.find("data", itemprop='Project[backers_count]')))
        self.pledged = removeHtml(str(self.soup.find('data', itemprop='Project[pledged]')))
        rawEndTime = str(self.soup.find('div', 'ksr_page_timer poll stat'))
        self.end_date = rawEndTime.split("data-end_time=")[1].split(' data-poll_url=')[0]
        # days_left = str(self.soup.find('div', 'ksr_page_timer poll stat'))

        self.location = removeHtml(str(self.soup.find_all('a', 'grey-dark mr3 nowrap')[0]))
        self.category = removeHtml(str(self.soup.find_all('a', 'grey-dark mr3 nowrap')[1]))

        self.mainVideoLink = str(self.soup.find('source', src=True)).split('<source src="')[1].split('" type=')[0]
        self.goal = removeHtml(str(self.soup.find('span', "money usd no-code")))

        self.updates = self.soup.find('div', "NS_projects_updates_section")
        commentSectionSoup = make_soup(BASE_URL + '/comments')
        self.comments = commentSectionSoup.find('ol', 'comments')

        self.faq = self.soup.find('ul', 'faqs')

        self.author_code = self.project_id + '_' + self.project_author.split(' ')[1]

        self.description = self.soup.find('div', 'full-description js-full-description responsive-media formatted-lists')
        self.risks = self.soup.find("div", "mb6")

        self.parseRewards()

        author_url = str(self.soup.find('a', 'remote_modal_dialog full_bio mr2', href=True))
        author_url = author_url.split('href="')[1]
        author_url = str(author_url.split('">See full bio</a>')[0])

        author = KickstarterAuthor(str('https://www.kickstarter.com') + author_url, self.project_id)

    def write_project_to_csv(self):
        exists = os.path.exists('project_TABLE.csv')
        with open('project_TABLE.csv', 'a') as csvfile:

            colHeaders = ['project_id', 'project_name', 'project_url', #'status',
                          'goal', 'end_date', 'author_code',
                          'location', 'category', 'video_link']
            writer = csv.DictWriter(csvfile, fieldnames=colHeaders)

            if not exists:
                writer.writeheader()

            writer.writerow({'project_id': str(self.project_id), \
                             'project_name': str(self.project_name), \
                             'project_url': str(self.pageurl), \
                             # 'status': str(status), \
                             'goal': str(self.goal), \
                             'end_date': str(self.end_date), \
                             'author_code': str(self.author_code), \
                             'location': str(self.location), \
                             'category': str(self.category), \
                             'video_link': str(self.mainVideoLink)})

    def write_project_update_csv(self):
        exists = os.path.exists('project_update_TABLE.csv')
        with open('project_update_TABLE.csv', 'a') as csvfile:

            colHeaders = ['project_id', 'pledged', 'num_backers', #'status',
                           'date', 'days_to_go',]
            writer = csv.DictWriter(csvfile, fieldnames=colHeaders)

            if not exists:
                writer.writeheader()

            writer.writerow({'project_id': str(self.project_id), \
                             'pledged': str(self.pledged), \
                             'num_backers': str(self.numBackers), \
                             # 'status': str(status), \
                             'date': str(self.date) \
                             # 'days_to_go': str(self),
                             })

if __name__ == '__main__':
    print "firing up";
    page = KicktstarterPage(BASE_URL)
    page.parsePage()
    page.write_project_to_csv()
    page.write_project_update_csv()


class KicktsarterPage:
    soup = None
    def __init__(self, url):
        soup = make_soup(url)

    def parsePage(self):
        projectName = self.soup.find("a", "green-dark")
        date = time.strftime("%d/%m/%Y")
        project_author = self.soup.find("a", "remote_modal_dialog green-dark")
        project_data = self.soup.find("data", "Project1165663259")
        print project_data
