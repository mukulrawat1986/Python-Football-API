#!/usr/bin/python

"""Python-Football-API, is a simple python wrapper around the Football-API"""


import urllib2
import urllib

from urlparse import urlparse
from urllib2 import HTTPError
from collections import namedtuple, OrderedDict

__author__ = "Mukul Rawat <rawatmukul86@gmail.com>"
__version__ = "1.0"


try:

    import simplejson
except ImportError:
    try:

        import json as simplejson
    except ImportError:
        try:

            from django.utils import simplejson
        except:
            raise Exception("Python-Football-API requires the simplejson/library to work")


class FootballApiErrors(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class FootballApi(object):

    def __init__(self, api_key):
        """         __init__(self, api_key)
        
                    Instantiates an instance of the FootballApi. Takes parameter for authentication
            
                    Parameters:
                        api_key: Your API key that authenticates you for requests against the Football-API
        """
        self.__base_url = "http://football-api.com/api/?"
        self.API_KEY = api_key
    
    
    def _checkResponse(self, res):
        """         _checkResponse(self, res)
        
                    Takes the returned JSON result from Football-API and checks it for odd errors, returning the repsonse if
                    everything checks out alright.
                    We are checking the returned JSON for the parameter ERROR.
                    
                    If ERROR == OK: Everything is fine
                    
                    Parameters:
                        res: A JSON object returned from the Football-API
                    
        """
        if res["ERROR"] == "OK":
            # everything is working
            return res
        elif res["ERROR"] == "API Key not found":
            
            raise FootballApiErrors("The API Key you entered is not found, check it")
        elif res["ERROR"] == "That Action cannot be found.  Did you send the 'Action' parameter?  List Actions with\
                                Action=DescribeActions":
            
            raise FootballApiErrors("There is a problem with the action mentioned, check it")
        elif res["ERROR"] == "The requested competition is not included in your subscription":
            
            raise FootballApiErrors("The competition is not in your subscription")
        elif res["ERROR"] == "Competition cannot be found":
            
            raise FootballApiErrors("Check the competition id")
        elif res["ERROR"] == "please specify the parameter 'match_date' or the two parameters 'from_date' \
                            and 'to_date' to get the matches":
            
            raise FootballApiErrors("Check the 'match_date' or 'from_date' and 'to_date'")
        elif res["ERROR"] == "Did not find any match today":
            
            raise FootballApiErrors("Check the 'match_date' or 'from_date' and 'to_date'")        
            
      
    def getCompetitions(self):
        """         getCompetitions(self)
        
                    Returns the list of competitions you are eligible for your current subscription plan
                    
                    Parameters:
                        None
        """
        params = OrderedDict()
        params["Action"] = "competitions"
        params["APIKey"] = self.API_KEY
        
        params = urllib.urlencode(params)
        
        res = simplejson.load(urllib2.urlopen(self.__base_url + "%s" % params))
        return self._checkResponse(res)["Competition"]
    
    
    def getStandings(self, comp_id):
        """         getStandings(self, comp_id)
        
                    Returns the league standing table for a given competition
                    
                    Parameters:
                        comp_id: Check out getCompetition() to see the list of competitons you are eligible for.
                        The "id" key is the competition id to be input here.
        
        """
        params = OrderedDict()
        params["Action"] = "standings"
        params["APIKey"] = self.API_KEY
        params["comp_id"] = comp_id
        
        params = urllib.urlencode(params)
        
        res = simplejson.load(urllib2.urlopen(self.__base_url + "%s" % params))
        return self._checkResponse(res)["teams"]
        
    def getToday(self, comp_id):
        """         getToday(self, comp_id)
        
                    Returns the matches scheduled today. This includes live matches and their updated events
                    
                    Parameters:
                        comp_id: Check out getCompetition() to see the list of competitions you are eligible for.
                        The "id" key is the competition id to be input here
        """
        params = OrderedDict()
        params["Action"] = "today"
        params["APIKey"] = self.API_KEY
        params["comp_id"] = comp_id
        
        params = urllib.urlencode(params)
        
        res = simplejson.load(urllib2.urlopen(self.__base_url + "%s" % params))
        return self._checkResponse(res)["matches"]
                
    
    def getFixtureDay(self, comp_id, match_date=None):
        """             getFixtureDay(self, comp_id, match_date)
        
                        Returns all the fixtures on a given date for a particular competition
                        
                        Parameters:
                            comp_id: Check out getCompetition() to see the list of competitions you are eligible for.
                            The "id" key is the competition id to be put here
                            
                            match_date: The particular day for which you want to find out all fixtures.
                            Date string should be of the form "dd.mm.yyyy" e.g "10.02.2015"
        """
                
        params = OrderedDict()
        params["Action"] = "fixtures"
        params["APIKey"] = self.API_KEY
        params["match_date"] = match_date 
        
        params = urllib.urlencode(params)
        
        res = simplejson.load(urllib2.urlopen(self.__base_url + "%s" % params))
        return self._checkResponse(res)["matches"]


    def getFixturePeriod(self, comp_id, from_date=None, to_date=None):
        """             getFixturePeriod(self, comp_id, from_date=None, to_date=None)
        
                        Returns all fixtures between the time period from_date and to_date for a particular
                        competition.
                        
                        Parameters:
                            comp_id: Check out getCompetitions to see the list of competitions you are eligible for.
                            The "id" key is the competition id to be put here.
                            
                            from_date: The particular day starting from which we want to know all the fixtures.
                            Date string should be of the form "dd.mm.yyy" e.g. "10.02.2015"

                            to_date: The particular day till which you want to find all the fixtures.
                            Date string should be of the form "dd.mm.yyyy" e.g. "10.02.2015"
    
        """
        params = OrderedDict()
        params["Action"] = "fixtures"
        params["APIKey"] = self.API_KEY
        params["from_date"] = from_date
        params["to_date"] = to_date

        params = urllib.urlencode(params)

        res = simplejson.load(urllib2.urlopen(self.__base_url + "%s" % params))
        return self._checkResponse(res)["matches"]


    def getCommentary(self, match_id):
        """             getCommentary(self, match_id)

                        Returns the live commentary if the match is on for a particular match.

                        Parameters:
                            match_id: The id of the match requested. You can get a particular match id by using the functions
                            getToday(), getFixtureDay() or getFixturePeriod()
        """
        params = OrderDict()
        params["APIKey"] = self.API_KEY
        params["match_id"] = match_id

        params = urllib.urlencode(params)

        res = simplejson.load(urllib2.urlopen(self.__base_url + "%s" % params))
        return self._checkResponse(res)
    


