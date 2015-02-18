from bs4 import BeautifulSoup
from urllib2 import urlopen
import time
import MySQLdb
import MySQLdb.cursors
import re

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
    db = None
    contact = None

    def __init__(self, url, project_id, db):

        authorSoup = make_soup(url)
        self.project_id = project_id
        self.full_name = removeHtml(str(authorSoup.find('span', 'identity_name')))
        self.location = removeHtml(str(authorSoup.find('p', 'h5 bold mb0')))
        self.bio = removeHtml(str(authorSoup.find('div', 'readability')))
        self.website = str(authorSoup.find('ul', 'links list h5 bold', href=True))
        self.db = db
        self.write_author_db()

    def write_author_db(self):
        c = self.db.cursor()
        c.execute("""SELECT series_number FROM project_table WHERE project_id = %s""", (self.project_id,))
        series_number = c.fetchall()
        args = (series_number, self.location, self.full_name, self.bio, self.contact)
        c.execute("""INSERT author_table (series_number, location, name, description, contact)
        VALUES(%s, %s, %s, %s, %s)""", args)
        self.db.commit()

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
    db = None

    def __init__(self, amount, numBackers, dDate, description, project_id, maxBackers, db):

        self.amount = amount
        self.numBackers = numBackers
        self.deliveryDate = dDate
        # self.shipsTo = shipsTo
        self.description = description
        self.project_id = project_id
        self.maxBackers = maxBackers
        self.db = db
        if self.maxBackers > 0:
            self.limited = True

        self.save_to_db()

    def save_to_db(self):
        c = self.db.cursor()
        c.execute("""SELECT series_number FROM project_table WHERE project_id = %s""", (self.project_id, ))
        series_number = c.fetchall()
        args = (series_number, self.amount, self.numBackers, self.deliveryDate, self.description, self.limited, (self.maxBackers))
        c.execute("""INSERT INTO rewards_table (series_number, pledge_amount, num_backers, delivery, description, limited, max_limit)
        VALUES(%s, %s, %s, %s, %s, %s, %s)""", args)
        self.db.commit()


class KicktstarterPage:
    #private memebrs
    soup = None
    project_url = None
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
    main_video_link = None
    goal = None
    rewards = None
    updates = None
    comments = None
    faq = None
    description = None
    risks = None
    db = None
    status = None
    days_to_go = None
    currency = None

    #methods
    def __init__(self, url, db):
        self.soup = make_soup(url)
        self.project_url = url
        self.db = db

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

            numBackers = re.findall(r'\d+', numBackers)[0]
            pledgeAmount = re.findall(r'\d+', pledgeAmount)[0]
            maxBackers = re.findall(r'\d+', maxBackers)[0]


            cleanReward = KickstarterReward(pledgeAmount, numBackers, delivery, description, self.project_id, maxBackers, self.db)

            rewardList.append(cleanReward)
        return rewardList

    def parsePage(self):
        self.project_id =  re.findall(r'\d+', str(self.soup.find('data', itemprop='Project[backers_count]')['class']))[0]

        urlExtension = self.project_url.replace('https://www.kickstarter.com' , '')
        self.project_name = removeHtml(str(self.soup.find('a', href=urlExtension)))
        self.date = time.strftime("%d/%m/%Y")
        self.project_author = removeHtml(str(self.soup.find('a', href=urlExtension + '/creator_bio')))
        self.numBackers = removeHtml(str(self.soup.find("data", itemprop='Project[backers_count]')))
        self.pledged = removeHtml(str(self.soup.find('data', itemprop='Project[pledged]')))
        self.pledged = re.findall(r'\d+', self.pledged)[0]
        rawEndTime = str(self.soup.find('div', 'ksr_page_timer poll stat'))
        if not rawEndTime is None:
            self.end_date = rawEndTime.split("data-end_time=")[1].split(' data-poll_url=')[0]
        # days_left = str(self.soup.find('div', 'ksr_page_timer poll stat'))

        self.location = removeHtml(str(self.soup.find_all('a', 'grey-dark mr3 nowrap')[0]))
        self.category = removeHtml(str(self.soup.find_all('a', 'grey-dark mr3 nowrap')[1]))

        self.main_video_link = self.soup.find('source', src=True)
        if not self.soup.find('source', src=True) is None:
            self.main_video_link = self.main_video_link['src']

        moneyStats = BeautifulSoup(str(self.soup.find('div', id='pledged')), 'lxml').find('data', 'Project' + str(self.project_id))

        self.currency = moneyStats.get('data-currency')

        self.goal = removeHtml(str(self.soup.find('span', 'money ' + str(self.currency).lower() + ' no-code')))

        self.updates = self.soup.find('div', "NS_projects_updates_section")
        commentSectionSoup = make_soup(self.project_url + '/comments')
        self.comments = commentSectionSoup.find('ol', 'comments')

        self.faq = self.soup.find('ul', 'faqs')


        self.description = self.soup.find('div', 'full-description js-full-description responsive-media formatted-lists')
        self.risks = self.soup.find("div", "mb6")

        # motherLoad = self.soup.find('div', self.project_id)
        # print motherLoad + '\n\n'

        # c = self.db.cursor()
        # c.execute("""SELECT project_id FROM project_table where project_id = %s""", (self.project_id,))
        # if not c.fetchone() is None:
        self.write_project_to_db()

        self.write_project_update_db()

    def write_project_to_db(self):
        c = self.db.cursor()
        args = (self.project_id, self.project_name, self.project_url, self.status, self.goal,
            self.end_date, self.project_author, self.location, self.main_video_link, self.category, self.currency)
        sql = ("""INSERT INTO project_table (project_id, project_name, project_url, status, goal, end_date, author_name,
        location, main_video_link, category, currency) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s);""")
        c.execute(sql, args)
        self.db.commit()
        # parse and write rewards
        self.parseRewards()
        #parse and write author information
        author_url = str(self.soup.find('a', 'remote_modal_dialog full_bio mr2', href=True))
        author_url = author_url.split('href="')[1]
        author_url = str(author_url.split('">See full bio</a>')[0])
        self.project_author = KickstarterAuthor(str('https://www.kickstarter.com') + author_url, self.project_id, self.db)

    def write_project_update_db(self):
        c = self.db.cursor()
        c.execute("""SELECT series_number FROM project_table WHERE project_id = %s""", (self.project_id,))
        series_num = c.fetchall()
        args = (series_num, self.pledged, self.numBackers, self.days_to_go, self.date)
        c.execute("""INSERT project_updates_table (series_number, pledged, num_backers, days_to_go, date) VALUES (%s, %s, %s, %s, %s);""", args)
        self.db.commit()

def scrape_this_page(page_url):

    print 'processing url: ' + page_url
    db = MySQLdb.connect(host="mysql.server", user="joeacanfora", passwd="password",db="joeacanfora$CrowdStore")

    page = KicktstarterPage(page_url, db)
    page.parsePage()