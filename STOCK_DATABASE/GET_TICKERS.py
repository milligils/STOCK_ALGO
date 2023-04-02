import pandas as pd
from stocksymbol import StockSymbol

class stocks:
    def __init__(self):
        pass
    
    def get_stock_data():
        api_key="6531297d-96e0-4dde-b69b-28a1886f9e7d"
        ss=StockSymbol(api_key)

        totalstocks_df=[]

        nasdaq=ss.get_symbol_list(index="IXIC", symbols_only=True)
        dowjones=ss.get_symbol_list(index="DJA", symbols_only=True)
        sp=ss.get_symbol_list(index="SPX", symbols_only=True)

        totalstocks=nasdaq+dowjones+sp

        totalstocks_df={"Symbol":totalstocks}
        totalstocks_df=pd.DataFrame(totalstocks_df).sort_values("Symbol", ascending=True)
        totalstocks_df.reset_index(inplace=True)
        del totalstocks_df['index']

        filename="TOTAL_STOCK_LIST.csv"
        totalstocks_df.to_csv("/Users/milligil/Desktop/"+filename, index=False)
        
        return totalstocks_df

if __name__ == '__main__':
    
    getstocks=stocks.get_stock_data()
    print(getstocks)