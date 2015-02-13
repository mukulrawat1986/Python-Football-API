#!/usr/bin/python

"""Python-Football-API is a simple python wrapper around the Football-API"""

import urllib
import urllib2
from collections import OrderedDict

__author__  = "Mukul Rawat <rawatmukul86@gmail.com>"
__version__ = "2.0"


try:
    import simplejson
except ImportError:
        try:
            import json as simplejson
        except ImportError:
            try:
                from django.utils import simplejson
            except ImportError:
                raise Exception("Python-Football-API requires simplejson library to work")


class FootballAPIErrors(Exception):
    
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return repr(self.msg)


class FootballAPI(object):
    
    def __init__(self, API_KEY):
        """         __init__(self, API_KEY)
        
                    Instantiates an instance of the FootballAPI class. Takes parameter
                    for instantiation.
                    
                    Parameters:
                        API_KEY: Your API Key that authenticates you for requests against
                        the Football-API
        """
        self._base_url = "http://football-api.com/api/?"
        self._API_KEY = API_KEY
    
    
    def _checkResponse(self, resp):
        """         _checkResponse(self, resp)
        
                    Takes the returned JSON result from Football-API and checks it for
                    odd errors, returning the repsonse if everything checks out alright.
                    We are checking the returned JSON for the parameter ERROR.
                    
                    Parameters:
                        res: A JSON object returned from the Football-API
        """
        if resp["ERROR"] == "OK":
            
            return resp
        elif resp["ERROR"] == "API Key not found":
            
            raise FootballAPIErrors("Error: The API Key you entered was not found")
        elif resp["ERROR"] == "That Action cannot be found.  Did you send the 'Action' \
                                parameter?  List Actions with Action=DescribeActions":
            
            raise FootballAPIErrors("Error: The Action mentioned couldn't be found")
        elif resp["ERROR"] == "The requested competition is not included in your \
                                subscription":
            
            raise FootballAPIErrors("Error: The competition is not in your subscription")
        elif resp["ERROR"] == "Competition cannot be found":
            
            raise FootballAPIErrors("Error: The competition cannot be found")
        elif resp["ERROR"] == "please specify the parameter 'match_date' or the two \
                            parameters 'from_date' and 'to_date' to get the matches":
            
            raise FootballAPIErrors("Error: Check the match_date or from_date and to_date")
        elif resp["ERROR"] == "Did not find any match today":
            
            raise FootballAPIErrors("Error: Check the match_date or from_date and to_date")
    
    
    def _callAPI(self, action=None, **kwargs):
        """         _callAPI(self, action=None, **kwargs)
        
                    This function is used to query the Football-API. The parameters passed
                    include the action to be performed and the parameters required for the
                    action.
                    
                    Parameters:
                        action: A string that specifies what action needs to be performed
                        **kwargs: An dictionary containing the parameters.
        """
        if action == None:
            raise FootballAPIErrors("Error: You forgot to mention action")
        
        params = OrderedDict()
        params["Action"] = action
        params["APIKey"] = self._API_KEY
        
        for kwarg in kwargs:
            params[kwarg] = kwargs[kwarg]
        
        params = urllib.urlencode(params)
        
        resp = simplejson.load(urllib2.urlopen(self._base_url + "%s" % params))
        return self._checkResponse(resp)
        
    
    def getCompetition(self):
        """         getCompetitions(self)
        
                    Returns the list of competitions you are eligible for your current subscription plan
                    
                    Parameters:
                        None
        """
        action = "competitions"
        return self._callAPI(action)
    
    
    def getStandings(self, comp_id=None):
        """         getStandings(self, comp_id=None)
                    
                    Returns the league standing table for a given competition
                    
                    Parameters:
                        comp_id: An integer specifying the id of the competition
        """
        if comp_id == None:
            raise FootballAPIErrors("Error: Enter the comp_id")
        
        action = "standings"
        params = {"comp_id": comp_id}
        return self._callAPI(action, **params)
    
    
    def getToday(self, comp_id=None):
        """         getToday(self, comp_id=None)
        
                    Returns the matches scheduled today. This includes live matches and
                    their updated events.
                    
                    Parameters:
                        comp_id: An integer specifying the id of the competition
        """
        if comp_id == None:
            raise FootballAPIErrors("Error: Enter the comp_id")
        
        action = "today"
        params = {"comp_id": comp_id}
        return self._callAPI(action, **params)  
    
    
    def getFixtureDay(self, comp_id=None, match_date=None):
        """         getFixtureDay(self, comp_id=None, match_date=None)
        
                    Returns the fixtures for a particular day.
                    
                    Parameters:
                        comp_id: An integer specifying the id of the competition
                        match_date: A string specifying the date of form "dd.mm.yyyy"
        """
        if comp_id == None:
            raise FootballAPIErrors("Error: Enter the comp_id")
        elif match_date == None:
            raise FootballAPIErrors("Error: Enter the match_date")
        
        action = "fixtures"
        params = { "comp_id": comp_id, "match_date": match_date }
        return self._callAPI(action, **params)
    
    
    def getFixturePeriod(self, comp_id=None, from_date=None, to_date=None):
        """         getFixturePeriod(self, comp_id=None, from_date=None, to_date=None)
        
                    Returns all fixtures between two given dates
                    
                    Parameters:
                        comp_id: An integer specifying the id of the competition
                        from_date: A string specifying starting date of form "dd.mm.yyyy"
                        to_date: A string specifying ending date of form "dd.mm.yyyy"
        """
        if comp_id == None:
            raise FootballAPIErrors("Error: Enter the comp_id")
        elif from_date == None:
            raise FootballAPIErrors("Error: Enter the from_date")
        elif to_date == None:
            raise FootballAPIErrors("Error: Enter the to_date")
        
        action = "fixtures"
        params = {"comp_id": comp_id, "from_date": from_date, "to_date": to_date}
        return self._callAPI(action, **params)
    
    
    def getCommentary(self, match_id=None):
        """         getCommentary(self, match_id=None)
        
                    Returns the commentary for a given match
                    
                    Parameters:
                        match_id: An integer which is the id of the match requested
        """
        if match_id == None:
            raise FootballAPIErrors("Error: Enter the match_id")
        
        action = "commentaries"
        params = {"match_id": match_id}
        return self._callAPI(action, **params)

