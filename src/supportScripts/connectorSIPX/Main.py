import requests
import pandas
import json
import time
import sqlite3
import schedule
import threading

from datetime import datetime, timedelta
from dateutil import parser

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
            
            conn.execute("INSERT INTO Market(NAME) VALUES ('SIPX') ON CONFLICT DO NOTHING");
            
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
        
        
def MAIN():
    
    E = ElecticityPrice()
    
    while True:
        print("Main Thread")
        time.sleep(1)
        print(E.GetPriceSIPX("2024-10-01T10:01:15"));
    
if __name__ == '__main__':
    MAIN()

