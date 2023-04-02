import mysql.connector as sql

class TableMaker():
    def __init__(self):        
        pass
    
    def one_table(self, db, tablename, columnnames):
        self.db=db
        self.tablename=tablename
        self.columnnames=columnnames
        
        self.tablename=self.tablename.replace(",", "")
        self.tablename=self.tablename.replace(".","")
        
        database=sql.connect(
            host="localhost",
            user="milligil",
            password="Manutd1@345",
            database=self.db
        )

        cursor=database.cursor()

        query="CREATE TABLE IF NOT EXISTS {table} ({columns})"
        query=query.format(table=tablename, columns=self.columnnames)

        cursor.execute(query)
        
    def multiple_tables(self, db, tablenames, columnnames):
        self.db=db
        self.tablenames=tablenames
        self.columnnames=columnnames

        database=sql.connect(
            host="localhost",
            user="milligil",
            password="Manutd1@345",
            database=self.db
        )

        cursor=database.cursor()

        for tablename in self.tablenames:
            tablename=tablename.replace(",", "")
            tablename=tablename.replace(".","")
            
            query="CREATE TABLE IF NOT EXISTS {table} ({columns})"
            query=query.format(table=tablename, columns=self.columnnames)

            cursor.execute(query)

if __name__ == '__main__':   
    db="stock_prices"
    column="Symbol"
    table="Stocks"
    
    tablename="META"
    tablenames=["AAA.", "AAB", "AAC"]
    
    columnnames=(   "CalendarDay VARCHAR(255), "
                    "TimeofDay VARCHAR(255), "
                    "Open_Price VARCHAR (255), "
                    "High_Price VARCHAR (255), "
                    "Low_Price VARCHAR (255), "
                    "Close_Price VARCHAR (255), "
                    "Volume VARCHAR (255), "
                    "VWAP VARCHAR (255), "
                    "Sma200 VARCHAR(255), "
                    "Sma50 VARCHAR (255), "
                    "Sma20 VARCHAR(255)"
                )

    tablemaker=TableMaker()
    #tablemaker.one_table(db, tablename, columnnames)
    
    SERVER='localhost'
    DB=db
    UID='milligil'
    PWD='Manutd1@345'
    
    cnx=sql.connect(user=UID, password=PWD, host=SERVER, database=DB)
    cursor=cnx.cursor()
    
    query="SELECT {column} from {table}"
    query=query.format(column=column, table=table)
    
    cursor.execute(query)
    all_records=cursor.fetchall()
    
    records=[]
    for row in all_records:
        row=str(row[0]).replace(",", "")
        
        records.append(row)
            
    tablemaker.multiple_tables(db, records, columnnames)

