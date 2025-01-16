import requests
import pandas
import json
import time
import sqlite3
import schedule
import threading

from datetime import datetime, timedelta
from dateutil import parser
from getTariff import gridPriceAtDatetime


class ElecticityPrice:
    
    def __init__(self):
    
        self.DB = "ElecticityMarket.db";
        
        self.initDataBase();
        self.initUpdateProcess();
        
        
    def initDataBase(self):
    
        with sqlite3.connect(self.DB) as conn:
        
            # conn.execute("DROP TABLE IF EXISTS Price");
            # conn.execute("DROP TABLE IF EXISTS Market");
            
            conn.execute(
            '''
                CREATE TABLE IF NOT EXISTS Market
                (
                    UUID INTEGER PRIMARY KEY,
                    NAME    TEXT NOT NULL,
                    UNIQUE(NAME)
                );
            ''');

            conn.execute(
            '''
                CREATE TABLE IF NOT EXISTS Price
                (
                    UUID INTEGER PRIMARY KEY,
                    MUID INTEGER NOT NULL,
                    TIME NUMERIC NOT NULL,
                    PRICE   REAL NOT NULL,
                    FOREIGN KEY (MUID) REFERENCES Market (UUID),
                    UNIQUE(MUID, TIME)
                );
            ''');
            
            conn.execute("INSERT INTO Market(NAME) VALUES ('SI') ON CONFLICT DO NOTHING");
            
            conn.commit();
        
    def initUpdateProcess(self):

        print("initUpdateProcess")
        
        s = schedule.Scheduler()
        
        s.every(30).seconds.do(self.UpdateSIPX)
        
        def run():
            
            s.run_all() # run all tasks on init
            
            while True:
                s.run_pending()
                time.sleep(1)
                
                print("Waiting...")
        
        t = threading.Thread(target=run)
        t.daemon = True
        t.start()
        
    def UpdateSIPX(self):
        
        print("Updating SIPX price");
        
        df = pandas.read_excel('https://www.bsp-southpool.com/sipx.html?file=files/documents/trading/SIPX_en.xlsx', skiprows = [0, 1], header = None)
        
        with sqlite3.connect(self.DB) as conn:
            for index, row in df.iterrows():
                for i in range(1, 25):
                    try:
                    
                        conn.execute(
                        '''
                            INSERT INTO 
                                Price
                                (
                                    MUID,
                                    TIME,
                                    PRICE
                                ) 
                            VALUES 
                                (?, ?, ?) 
                            ON CONFLICT
                                (
                                    MUID,
                                    TIME
                                )
                            DO UPDATE SET 
                                Price = ?
                                
                        ''', (1, (row[0] + timedelta(hours=i)).timestamp(), row[i], row[i], ))
                    except Exception as e:
                        print(e)
            
            conn.commit();
        
    def GetPriceSIPX(self, TimeStamp):
        
        unixTime = int(parser.parse(TimeStamp).timestamp())
        
        with sqlite3.connect(self.DB) as conn:
            X = conn.execute("SELECT * FROM Price WHERE TIME <= ? ORDER BY TIME DESC LIMIT 1", (unixTime, ));
            
            return X.fetchone()
        
        return None
        
    def GetPriceCatalogSIPX(self):
        """
        Retrieves the price catalog for the 'SI' market from the database.
    
        This method connects to the SQLite database specified by the instance's 
        DB attribute and executes a SQL query to fetch the latest 48 price records 
        for the market named 'SI'. The query uses a window function to get the 
        previous price time for each record.
    
        The results are processed to convert the timestamps from Unix format to 
        ISO 8601 format with a 'Z' suffix indicating UTC time.
    
        Returns:
            list: A list of dictionaries, each containing the price, previous 
                  price time, and current time in ISO 8601 format. Returns None 
                  if no records are found.
        """
        with sqlite3.connect(self.DB) as conn:
            conn.row_factory = sqlite3.Row
            
            X = conn.execute(
            '''
                SELECT
                    PRICE AS P,
                    LAG (TIME, 1, 0) OVER (PARTITION BY MUID ORDER BY TIME) AS F,
                    TIME AS T
                FROM
                    PRICE
                INNER JOIN
                    MARKET
                    ON
                    MARKET.UUID = PRICE.MUID
                WHERE
                    MARKET.NAME = 'SI'
                ORDER BY
                    TIME DESC
                LIMIT 48;
            ''')
            
            dictList = [dict(ix) for ix in X.fetchall()]
            
            for item in dictList:
                item['F'] = datetime.utcfromtimestamp(item['F']).isoformat() + 'Z'
                item['T'] = datetime.utcfromtimestamp(item['T']).isoformat() + 'Z'
        
            return dictList
        
        return None
        
    def GetAdjustedPrices(self):
        """
        Retrieves the adjusted prices for the 'SI' market from the database.

        This method connects to the SQLite database specified by the instance's 
        DB attribute and executes a SQL query to fetch the adjusted price records 
        for the market named 'SI'. The results are processed to convert the 
        timestamps from Unix format to ISO 8601 format with a 'Z' suffix indicating UTC time.

        Returns:
            dict: A dictionary containing a list of adjusted prices with their 
                corresponding timestamps. The format is:
                {
                    "prices": [
                        {"time": "2025-01-16T00:00:00Z", "price": 0.10},
                        ...
                    ]
                }
            Returns an empty dictionary if no records are found.
        """
        with sqlite3.connect(self.DB) as conn:
            conn.row_factory = sqlite3.Row
            
            X = conn.execute(
            '''
                  SELECT
                    PRICE AS P,
                    LAG (TIME, 1, 0) OVER (PARTITION BY MUID ORDER BY TIME) AS F,
                    TIME AS T
                FROM
                    PRICE
                INNER JOIN
                    MARKET
                    ON
                    MARKET.UUID = PRICE.MUID
                WHERE
                    MARKET.NAME = 'SI'
                ORDER BY
                    TIME DESC
                LIMIT 48;
            ''')
            
            dictList = [{"time": datetime.utcfromtimestamp(row['T']).isoformat() + 'Z', 
                          "price": addMockupAndGrid(row['P'],row['T'])} for row in X.fetchall()]
        
        return {"Prices": dictList}   

def addMockupAndGrid(price,dateTime):
    mockup = 0.015
#    print(gridPriceAtDatetime(dateTime))    
    return round(price/1000 + mockup, 5)

def MAIN():
    
    E = ElecticityPrice()

    '''  
    while True:
        print("Main Thread")
        time.sleep(1)
        print(E.GetPriceSIPX("2024-10-01T10:01:15"));
        print(E.GetPriceCatalogSIPX());
        
    '''         
    dt = "2025-01-16T13:01:15"
    print(E.GetPriceSIPX(dt))

    print(addMockupAndGrid(gridPriceAtDatetime(dt),dt))
     

if __name__ == '__main__':
    MAIN()

