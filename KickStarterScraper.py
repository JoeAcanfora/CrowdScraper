__author__ = 'joeacanfora'


import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class KickStarterItem(scrapy.item):
    pageurl = scrapy.Field()
    projectName = scrapy.Field()
    companyName = scrapy.Field()
    numBackers = scrapy.Field()
    pledgeAmount = scrapy.Field()
    pledgeGoal = scrapy.Field()
    daysToGo = scrapy.Field()
    description = scrapy.Field()
    location = scrapy.Field()
    category = scrapy.Field()
    rewards = scrapy.Field()
    videoUrl = scrapy.Field()
    risks = scrapy.Field()


class KickStarterSpider(CrawlSpider):

    name = 'kickstarter'
    allowed_domains = ['kickstarter.com']
    start_urls = ['https://www.kickstarter.com/projects/1122924030/visr-virtual-reality']
    rules = [Rule(LinkExtractor(allow=['/tor/\d+']), 'prase_kickstart')]

    def parse_kickstart(self, response):
        kickSt = KickStarterItem()
        kickSt['url'] = response.url
