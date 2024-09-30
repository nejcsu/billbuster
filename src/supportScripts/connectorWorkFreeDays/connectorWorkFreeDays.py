import requests
import json
from datetime import datetime
from datetime import date

class WorkFreeDays:
    
    def __init__(self, iso2):
        
        self.HOST = "https://date.nager.at/api/v3/PublicHolidays";
        
        self.ISO2 = iso2
        
        print("WorkFreeDays")
    
    # TODO: Save API responses and optimize code
    def getPublicHolidays(self, isoDate):
        
        isPublicHoliday = False;
        
        URL = "%s/%d/%s" % (self.HOST, isoDate.year, self.ISO2)
        
        print(URL);
        
        response = requests.request("GET", URL)
        
        print(response.text)
        
        print(isoDate.isoformat())
        
        for day in json.loads(response.text):
            if(day["date"] == isoDate.isoformat()):
                isPublicHoliday = True;
                
        return isPublicHoliday;
        
    def getDayInfo(self, DATE):
        
        isoDate = date.fromisoformat(DATE)
        
        dayInfo = { "WorkFreeDay": False }
        
        print(isoDate.month)
        
        if(isoDate.weekday() == 5): dayInfo["WorkFreeDay"] = True; # Saturday
        if(isoDate.weekday() == 6): dayInfo["WorkFreeDay"] = True; # Sunday
        
        if(dayInfo["WorkFreeDay"] == False):
            dayInfo["WorkFreeDay"] = self.getPublicHolidays(isoDate)
            
        return dayInfo;

def TEST():
    
    countryIso2 = "SI";
    
    API = WorkFreeDays(countryIso2)
    
    print(API.getDayInfo("2024-10-08")) # Normal working day
    print(API.getDayInfo("2024-11-01")) # Public holiday - 1st november
    print(API.getDayInfo("2024-10-12")) # Weekend - saturday
    
    # TODO: Unit tests
    
    
TEST()
