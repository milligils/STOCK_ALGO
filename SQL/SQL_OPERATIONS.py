import mysql.connector as sql
import pandas as pd
from GET_STOCK_DATA import StockInfo as si

class SQLOps:
    def __init__(self):
        pass
    
    def upload_new_prices(self, stock, column_names, period_poly, periodtype_poly, start, end):
        self.stock=stock
        self.period_poly=period_poly
        self.periodtype_poly=periodtype_poly
        self.column_names=column_names
        self.start=start
        self.end=end
        
        try:
            stockinfo = si().get_prices_polygon(self.stock, self.period_poly, self.periodtype_poly, self.start, self.end)
            stockinfo["Day"]=stockinfo["Day"].astype(str)
            stockinfo["Time"]=stockinfo["Time"].astype(str)
            
            stockinfo=stockinfo.to_dict('index')
            
            HOST="127.0.0.1"
            SERVER='localhost'
            DB='stock_prices'
            UID='milligil'
            PWD='Manutd1@345'
            
            cnx=sql.connect(user=UID, password=PWD, host=SERVER, database=DB)
            cursor=cnx.cursor()
            query="INSERT INTO {table} ({columnnames}) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            query=query.format(table=stock, columnnames=self.column_names)
            
            for key in stockinfo:
            
                current_day=stockinfo[key]["Day"]
                current_time=stockinfo[key]["Time"]
                current_open=stockinfo[key]["Open"]
                current_high=stockinfo[key]["High"]
                current_low=stockinfo[key]["Low"]
                current_close=stockinfo[key]["Close"]
                current_vol=stockinfo[key]["Volume"]
                
                cursor.execute(query, (current_day, current_time, current_open, current_high, current_low, current_close, current_vol))
                cnx.commit()
            cnx.close()
            
        except:
            print(stock+" didn't work.")
            
    def obtain_data(self, db, columns, table):
        self.db=db
        self.columns=columns
        self.table=table
        
        SERVER='localhost'
        DB=self.db
        UID='milligil'
        PWD='Manutd1@345'
        
        cnx=sql.connect(user=UID, password=PWD, host=SERVER, database=DB)
        cursor=cnx.cursor()
        
        query="SELECT {column} from {table}"
        query=query.format(column=self.columns, table=self.table)
        cursor.execute(query)
        all_records=cursor.fetchall()
        
        records=[]
        for row in all_records:
            records.append(str(row[0]).replace(",", ""))
            
        return records
    
    def delete_all_entries(self, db):
        self.db=db
        
        SERVER='localhost'
        DB=self.db
        UID='milligil'
        PWD='Manutd1@345'
        
        cnx=sql.connect(user=UID, password=PWD, host=SERVER, database=DB)
        cursor=cnx.cursor()
        
        query="SELECT * from Stocks"
        cursor.execute(query)
        all_records=cursor.fetchall()
        
        records=[]
        for row in all_records:
            records.append(str(row[1]).replace(",", ""))
                    
        for record in records:
            record=record.replace(".", "")
            
            try:
                query="DELETE FROM {table}"
                query=query.format(table=record)
                            
                cursor.execute(query)
            except:
                print(str(record)+"did not work")
        
if __name__ == '__main__':
    stock="AMC"
    period="6mo"
    frequency="1h"
    db="stock_prices"
    columnnames=(   "CalendarDay, "
                    "TimeofDay, "
                    "Open_Price, "
                    "High_Price, "
                    "Low_Price, "
                    "Close_Price, "
                    "Volume"
                )
    
    #test=SQLOps().upload_new_prices(stock, columnnames, period, frequency)
    
    #test2=SQLOps().obtain_current_entries(db)
    
    #test3=SQLOps().delete_all_entries(db)
    
