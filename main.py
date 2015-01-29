from bs4 import BeautifulSoup
from urllib2 import urlopen
import time
import csv

BASE_URL = "https://www.kickstarter.com/projects/arduinoclassroomkit/arduino-based-electronics-discovery-system-duinoki?ref=category_location"

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

class KickstarterReward:

    amount = None
    limited = None
    maxBackers = None
    numBackers = None
    deliveryDate = None
    shipsTo = None
    description = None

    def __init__(self, amount, numBackers, dDate, shipsTo, description):

        self.amount = amount
        self.numBackers = numBackers
        self.deliveryDate = dDate
        self.shipsTo = shipsTo
        self.description = description


class KicktstarterPage:
    soup = None
    pageurl = None


    def __init__(self, url):
        self.soup = make_soup(url)
        self.pageurl = url

    def parseRewards(self):
        rewardList = []
        rawRewards = self.soup.findAll("li", "NS-projects-reward bg-grey-light rounded clip mb2 relative")
        for rawR in rawRewards:
            sideSoup = BeautifulSoup(str(rawR), "lxml")
            reward = KickstarterReward(BeautifulSoup(str(sideSoup.find("h5", "mb1"))).findAll(text=True), \
                     BeautifulSoup(str(sideSoup.find("span", "num-backers mr1"))).findAll(text=True), \
                     BeautifulSoup(str(sideSoup.find("div", "delivery-date h6"))).findAll(text=True), \
                     BeautifulSoup(str(sideSoup.find("div", "NS_backer_rewards__shipping"))).findAll(text=True), \
                     BeautifulSoup(str(sideSoup.find("div", "desc h5 mb2 break-word"))).findAll(text=True))
            rewardList.append(reward)
        return rewardList

    def parsePage(self):
        projectName = removeHtml(str(self.soup.find("a", "green-dark")))
        date = time.strftime("%d/%m/%Y")
        project_author = removeHtml(str(self.soup.find("a", "remote_modal_dialog green-dark")))
        projectData = [data.string for data in self.soup.findAll("data", "Project1165663259")]
        numBackers = removeHtml(str(projectData[0]))
        totalRaisedToDate = removeHtml(str(projectData[1]))
        currency = "TODO"
        daysToGo = removeHtml(str(self.soup.find("div" "num h1 bold")))
        description = "TODO"
        category = removeHtml(str(self.soup.find("span", "ss-icon ss-tag margin-right")))
        location = removeHtml(str(self.soup.find("a", "grey-dark mr3 nowrap")))
        mainVideoLink = removeHtml(str(self.soup.find("video", "has_webm landscape" )))
        rewards = self.parseRewards()
        risks = removeHtml(str(self.soup.find("div", "mb6")))
        # updates =
        # comments =
        # faq =

        with open("crowProject.csv", 'w') as csvfile:
            colHeaders = ['Date', 'Project_Name', 'Project_Author', 'Total_Backers', 'Total_Raised', \
                          'Currency', 'Days_To_Go', 'Description', 'Location', 'Category', 'Video_Link', 'Risks']
            writer = csv.DictWriter(csvfile, fieldnames=colHeaders)
            writer.writeheader()
            writer.writerow({'Date': str(date), \
                             'Project_Name': str(projectName), \
                             'Project_Author': str(project_author), \
                             'Total_Backers': str(numBackers), \
                             'Total_Raised' : str(totalRaisedToDate), \
                             'Currency': str(currency), \
                             'Days_To_Go': str(daysToGo), \
                             'Description': str(description), \
                             'Location': str(location), \
                             'Category': str(category), \
                             'Video_Link': str(mainVideoLink), \
                             'Risks': str(risks)})

if __name__ == '__main__':
    print "firing up";
    page = KicktstarterPage(BASE_URL)
    page.parsePage()



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
