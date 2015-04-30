'''
Created on Oct 20, 2013

@author: Jon
'''
#modified by Joe Acanfora March 24th, 2015
#purpose to is get a list of kickstarter campaign urls for a given category.

import requests, time

class KickAPIClass():
    '''
    This is a port of the Kickscraper Rubygem to Python.
    It's designed to work under a slightly different set of constraints, but it works similarly.

    When called, it generates an api token for you and pulls all your custom-signed urls from the basic api call. These are saved throughout the session
    Currently this doesn't actually do anything with the results... it's meant to be called by another script
    '''

    def __init__(self,email,password):
        '''
        This generates an oauth api token that the program uses to make the initial call. Currently the token is only useful for that one call, but it is kept in case
        '''
        self.cat = []
        self.cats = []
        self.successful = False
        self.access_token = ""
        url = "https://api.kickstarter.com"
        self.headers = {'Accept' : "application/json, text/javascript; charset=utf-8"}#, 'User-Agent' : "PyKick/XXX"}
        auth_url = url+"/xauth/access_token?client_id=2II5GGBZLOOZAA5XBU1U0Y44BU57Q58L8KOGM7H0E0YFHP3KTG"
        token_response = ""
        try:
            token_response = requests.post(auth_url, headers = self.headers, verify = False, data = {'email' : email, 'password' : password })
            print "token responsed successfully"
            # print token_response.json()
            self.access_token = token_response.json()["access_token"]
            print "access token grabbed successfully"
            # print self.access_token
            time.sleep(2)
            url_url = "https://api.kickstarter.com/v1/?oauth_token="+self.access_token
            url_response = requests.get(url_url,headers = self.headers)
            self.successful = True
            return None
        except:
            print token_response.status_code
            return None


    def track_category(self, cat_name = "Technology", cat_id = 35):

		game_page = 1
		total_hits = 1
		hits_parsed = 0
		more_to_discover = True
		projs = []
		while (more_to_discover is True) and (hits_parsed < total_hits) and (hits_parsed < 250):
			hits_parsed = hits_parsed + 20 #naive assumption that projects length is always going to be
			discover_category = requests.get("http://www.kickstarter.com/discover/categories/" + cat_name + '?sort=newest', headers = self.headers, params = {"page":game_page})
			try:
			    dscCat = discover_category.json()
			except Exception, e:
			    print str(e)
			    time.sleep(4)
			    break
			total_hits = dscCat["total_hits"]
			print discover_category.status_code
			if discover_category.status_code != 200:
				more_to_discover = False
				# print discover_category.text

			else:
				for project in dscCat["projects"]:
					try:
					   # print project
					    thisProj = {}
					    thisProj["id"] 					= project["id"]
					    thisProj["creator"] 		= project["creator"]["name"]
					    thisProj["location"] 		= project["location"]["short_name"]
					    thisProj["state"] 			= project["state"]
					    thisProj["deadline"] 		= project["deadline"]
					    thisProj["launched_at"] = project["launched_at"]
					    thisProj["name"] 				= project["name"]
					    thisProj["blurb"]				= project["blurb"]
					    thisProj["link"] 				= project["urls"]["web"]["project"]
					    thisProj["goal"]				= project["goal"]
					    thisProj["pledged"]			= project["pledged"]
					    thisProj["currency"]		= project["currency"]
					    thisProj["currency_symbol"]		= project["currency_symbol"]
					    thisProj["currency_trailing_code"]		= project["currency_trailing_code"]
					    projs.append(thisProj)
					    print str(hits_parsed) + "/" + str(total_hits) + ": " + thisProj["link"]
					    print thisProj["launched_at"]

					except Exception, e:
						print str(e)
						print "failure!!"
						print discover_category.text
						print "failure!!"
						print
						time.sleep(15)
				game_page = game_page+1
				time.sleep(4)
		return projs

# mc = KickAPIClass("login@login.login","secrectpassword!")