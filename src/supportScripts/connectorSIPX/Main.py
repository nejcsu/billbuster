import requests
import pandas
import json
import sqlite3

from datetime import datetime, timedelta
from dateutil import parser

class ElecticityPrice:
    
    def __init__(self):
        
        self.sql = sqlite3.connect("ElecticityMarket.db");
        
        # self.sql.execute("DROP TABLE IF EXISTS Price");
        # self.sql.execute("DROP TABLE IF EXISTS Market");
        
        self.sql.execute(
        '''
            CREATE TABLE IF NOT EXISTS Market
            (
                UUID INTEGER PRIMARY KEY,
                NAME    TEXT NOT NULL,
                UNIQUE(NAME)
            );
        ''');

        self.sql.execute(
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
        
        self.sql.execute("INSERT INTO Market(NAME) VALUES ('SIPX') ON CONFLICT DO NOTHING");
        
        self.sql.commit();
        
        self.UpdateSIPX();
        
    def UpdateSIPX(self):
        
        df = pandas.read_excel('https://www.bsp-southpool.com/sipx.html?file=files/documents/trading/SIPX_en.xlsx', skiprows = [0, 1], header = None)
        
        for index, row in df.iterrows():
            for i in range(1, 25):
                try:
                
                    self.sql.execute(
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
        
        self.sql.commit();
        
    def GetPriceSIPX(self, TimeStamp):
        
        unixTime = int(parser.parse(TimeStamp).timestamp())
        
        X = self.sql.execute("SELECT * FROM Price WHERE TIME <= ? ORDER BY TIME DESC LIMIT 1", (unixTime, ));
        
        row = X.fetchone()
        
        return (row[3])
        
def MAIN():
    
    E = ElecticityPrice()
    
    print(E.GetPriceSIPX("2024-10-01T10:01:15"));
    
MAIN()

