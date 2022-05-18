import yfinance as yf
import pandas as pd
import streamlit as st
from stocksymbol import StockSymbol
import os
from dotenv import load_dotenv

load_dotenv()

class StreamlitFrontEnd:
    def __init__(self, api_key):
        #store all stocks in memory
        self.api_key = api_key
        self.ss = StockSymbol(self.api_key)
        self.marketList = self.ss.market_list
        self.indexList = self.ss.index_list
        
        self.markets = list()
        self.indices = dict()
        self.indexIDs = dict()
        
        for i in self.marketList:
            self.indices[i["market"]] = list()
            temp = "("+ i["abbreviation"] + ") " + i["market"]
            self.markets.append(temp)
        self.markets.insert(0, self.markets.pop()) #defaults america to top of list for convenience
            
        for i in self.marketList:
            indicesByMarket = i["index"]
            for j in indicesByMarket:
                self.indices[i["market"]].append(j["name"])
                self.indexIDs[j["name"]] = j["id"][1 + j["id"].index(":"):]
                
        for i in self.indices:
                self.indices[i].insert(0, "-") #options to search all indices
        
        marketSelectBox = st.sidebar.selectbox("Select a Market", self.markets, key="marketSelectBox")
        indexSelectBox = st.sidebar.selectbox("Select an Index", self.indices[self.updateIndexList(marketSelectBox)], key="indexSelectBox")
        companySelectBox = st.selectbox("Select a Company", self.updateCompanyList(marketSelectBox, indexSelectBox), key="companySelectBox")
        stockInfoBox = st.info(self.getStockDF(companySelectBox))
        
    def updateCompanyList(self, marketSelectBox, indexSelectBox):
        if(indexSelectBox == "-"):
            return self.updateCompanyList2(marketSelectBox)
        else:
            id = self.indexIDs[indexSelectBox]
            symbolListByID = self.ss.get_symbol_list(index = id)
            toReturn = list()
            for i in symbolListByID:
                temp = "(" + i["symbol"] + ") " + i["longName"]
                toReturn.append(temp)
            return toReturn
                
    def updateCompanyList2(self, marketSelectBox):
        symbolListByMarket = self.ss.get_symbol_list(market = marketSelectBox[1:3])
        toReturn = list()
        for i in symbolListByMarket:
            temp = "(" + i["symbol"] + ") " + i["longName"]
            toReturn.append(temp)
        return toReturn            
    
    def updateIndexList(self, marketSelectionBox):
        temp = marketSelectionBox
        temp = temp[5:]
        return temp
    
    def getStockTicker(self, companySelectBox):
        temp = companySelectBox
        temp = temp[1:temp.index(")")]
        return temp
    
    def getStockDF(self, companySelectBox):
        ticker = self.getStockTicker(companySelectBox)
        stock = yf.Ticker(ticker)
        st.dataframe(stock.history("1y"))
        st.line_chart(stock.history("1y").loc[:,"Close"])
    
stonk = StreamlitFrontEnd(os.getenv("api_key"))