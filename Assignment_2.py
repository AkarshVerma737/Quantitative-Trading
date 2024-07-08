from statsmodels.tsa.stattools import adfuller
import pandas as pd
import numpy as nb
import matplotlib.pyplot as plt
import yfinance as yf

def Create_stock(s):
    stock = yf.download(s, start="2021-05-25", end="2023-05-25",group_by='tickers')
    df = pd.DataFrame(stock)
    df = df.drop(columns=["Adj Close","Volume"])
    df = df.assign(Z_Score = 0)

    return df


#To test the stationarity of the series using ADF Test

def adf(df):
    df = df.drop(df[df.index < "2023-01-01"].index , axis = 0)
    result = adfuller (df, autolag='AIC')
    if (result[1]<0.05):
        print("STATIONARY")
    else:
        print("NON STATIONARY")


#To plot the Z-Score

def z(df1,df2):
    df1 = df1.drop(df1[df1.index < "2023-01-01"].index , axis = 0)
    df2 = df2.drop(df2[df2.index < "2023-01-01"].index , axis = 0)
    df = df1.Close/df2.Close
    m=df.mean()
    s=df.std()
    df1=df1.assign(Z_Score = (df - m)/s)
    m=df1.Z_Score.mean()
    s=df1.Z_Score.std()
    plt.plot(df1.index , df1.Z_Score , color = 'black' , label = "Z Score")
    plt.axhline(y = m , color='r', label = "Mean")
    plt.axhline(y = m+2*s , color = 'b', label = "Mean +/- 2*Standard Deviation")
    plt.axhline(y = m-2*s , color = 'b')
    plt.xticks(rotation=45, ha = 'right')
    plt.legend()
    plt.show()


#To Find Sharpe Ratio

def sr(df):
    df = df.drop(df[df.index < "2022-05-25"].index , axis = 0)
    df = df.assign(Daily_Return = 0)
    df[['Daily_Return']] = df[['Close']].diff()
    sp = df['Daily_Return'].mean()/df['Daily_Return'].std()
    print("\nSharpe Ratio for AMD Stock is:\t",sp)


#To find when Golden Cross and Death Cross Occur

def gcdc(df):
    df = df.assign(Cldiff = df[['Close']].diff())
    df = df.assign(NET = df.Open * df.Cldiff / (df.Close - df.Cldiff))
    df = df.assign(AVG_15_Day = df['NET'].rolling(15).mean())
    df = df.assign(AVG_50_Day = df['NET'].rolling(50).mean())
    c1 = 0
    c2 = 0
    gc=[]
    dc=[]
    if(df.AVG_15_Day[50]>df.AVG_50_Day[50]):
        c1=1
    else:
        c2=1
    for x in range(50,503):
        if (df.AVG_15_Day[x]>df.AVG_50_Day[x] and c2==1):
            gc.append(df.index[x])
            c2=0
            c1=1
        if (df.AVG_15_Day[x]<df.AVG_50_Day[x] and c1==1):
            dc.append(df.index[x])
            c1=0
            c2=1
    print("\nGolden Cross at :\n",gc)
    print("\nDeath Cross at :\n",dc)


#Input and function calls

df1=Create_stock("BAJAJFINSV.NS")
df2=Create_stock("HERO")
df3=Create_stock("AMD")
df4=Create_stock("IBM")

stock = {"BajajFinance":df1 , "HERO":df2 , "AMD":df3 , "IBM":df4}
for x in stock:
    adf(stock[x].drop(columns=["Open","High","Low","Z_Score"]))

z(stock["HERO"],stock["BajajFinance"])
z(stock["AMD"],stock["IBM"])

sr(stock["AMD"].drop(columns=["Open","High","Low","Z_Score"]))

gcdc(stock["AMD"].drop(columns=["High","Low","Z_Score"]))
