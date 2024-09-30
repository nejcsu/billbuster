import requests

class MojElektro:
    
    # Swagger: https://docs.informatika.si/mojelektro/api
    
    # Topologija:
    # MerilnoMesto > 1..* > MerilnaTocka
    # MerilnoMesto > 1..* > MeterReadings
    
    def __init__(self, key):
        
        self.HOST = "https://api.informatika.si/mojelektro/v1/";
        
        self.AKEY = key
        
        print("Moj Elektro API")
        
    def getMerilnoMesto(self, MMID):
        
        URL = "%s/merilno-mesto/%s" % (self.HOST, MMID)
        
        print(URL);
        
        headers = { 'x-api-token': self.AKEY }
        
        response = requests.request("GET", URL, headers = headers)
        
        print(response.text)
        
    def getMerilnaTocka(self, GSRN):
        
        URL = "%s/merilna-tocka/%s" % (self.HOST, GSRN)
        
        print(URL);
        
        headers = { 'x-api-token': self.AKEY }
        
        response = requests.request("GET", URL, headers = headers)
        
        print(response.text)
        
    def getMeterReadings(self, MMID):
        
        
        URL = "%s/meter-readings" % (self.HOST)
        
        par = { "usagePoint": MMID, "option": [] }
        
        par["startTime"] = "2024-09-24"
        par["endTime"  ] = "2024-09-27"
        
        par["option"].append("ReadingType=32.0.2.4.1.2.12.0.0.0.0.0.0.0.0.3.72.0" ) # Prejeta 15 minutna delovna energija
        par["option"].append("ReadingType=32.0.2.4.19.2.12.0.0.0.0.0.0.0.0.3.72.0") # Oddana 15 minutna delovna energija
        par["option"].append("ReadingType=32.0.2.4.1.2.12.0.0.0.0.0.0.0.0.3.73.0" ) # Prejeta 15 minutna jalova energija
        par["option"].append("ReadingType=32.0.2.4.19.2.12.0.0.0.0.0.0.0.0.3.73.0") # Oddana 15 minutna jalova energija
        par["option"].append("ReadingType=32.0.2.4.1.2.37.0.0.0.0.0.0.0.0.3.38.0" ) # Prejeta 15 minutna delovna moč
        par["option"].append("ReadingType=32.0.2.4.19.2.37.0.0.0.0.0.0.0.0.3.38.0") # Oddana 15 minutna delovna moč
        par["option"].append("ReadingType=32.0.2.4.1.2.37.0.0.0.0.0.0.0.0.3.63.0" ) # Prejeta 15 minutna jalova moč
        par["option"].append("ReadingType=32.0.2.4.19.2.37.0.0.0.0.0.0.0.0.3.63.0") # Oddana 15 minutna jalova moč
        par["option"].append("ReadingType=32.0.4.1.1.2.12.0.0.0.0.0.0.0.0.3.72.0" ) # Prejeta delovna energija ET
        par["option"].append("ReadingType=32.0.4.1.1.2.12.0.0.0.0.1.0.0.0.3.72.0" ) # Prejeta delovna energija VT
        par["option"].append("ReadingType=32.0.4.1.1.2.12.0.0.0.0.2.0.0.0.3.72.0" ) # Prejeta delovna energija MT
        par["option"].append("ReadingType=32.0.4.1.19.2.12.0.0.0.0.0.0.0.0.3.72.0") # Oddana delovna energija ET
        par["option"].append("ReadingType=32.0.4.1.19.2.12.0.0.0.0.1.0.0.0.3.72.0") # Oddana delovna energija VT
        par["option"].append("ReadingType=32.0.4.1.19.2.12.0.0.0.0.2.0.0.0.3.72.0") # Oddana delovna energija MT
        par["option"].append("ReadingType=32.0.4.1.1.2.12.0.0.0.0.0.0.0.0.3.73.0" ) # Prejeta jalova energija ET
        par["option"].append("ReadingType=32.0.4.1.1.2.12.0.0.0.0.1.0.0.0.3.73.0" ) # Prejeta jalova energija VT
        par["option"].append("ReadingType=32.0.4.1.1.2.12.0.0.0.0.2.0.0.0.3.73.0" ) # Prejeta jalova energija MT
        par["option"].append("ReadingType=32.0.4.1.19.2.12.0.0.0.0.0.0.0.0.3.73.0") # Oddana jalova energija ET
        par["option"].append("ReadingType=32.0.4.1.19.2.12.0.0.0.0.1.0.0.0.3.73.0") # Oddana jalova energija VT
        par["option"].append("ReadingType=32.0.4.1.19.2.12.0.0.0.0.2.0.0.0.3.73.0") # Oddana jalova energija MT

        
        print(URL);
        
        headers = { 'x-api-token': self.AKEY }
        
        response = requests.request("GET", URL, headers = headers, params = par)
        
        print(response.text)
        


def TEST():
    
    merilnoMestoID = "#-######";
    merilnaTockaID = "##############";
    
    ApiKey = "##SomeKey##";
    
    API = MojElektro(ApiKey)
    
    API.getMerilnoMesto(merilnoMestoID)
    API.getMeterReadings(merilnoMestoID)
    API.getMerilnaTocka(merilnaTockaID)
    
    
TEST()
