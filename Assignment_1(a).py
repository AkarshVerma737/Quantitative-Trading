import pandas as pd
import yfinance as yf

def Create_stock(s):
    stock = yf.download(s, start="2022-01-01", end="2023-01-31",group_by='tickers')
    df = pd.DataFrame(stock)
    df = df.drop(columns=["Adj Close","Volume"])
    df = df.assign(OPEN_CLOSE=df.Open/df.Close,OPEN_LOW=df.Open/df.Low,HIGH_LOW=df.High/df.Low,HIGH_CLOSE=df.High/df.Close)
    return df

def Find_Ratio(df,st,n):
    c=0
    for row in df[st]:
        if row == n:
            c=c+1
    return c

def printratio (df,n):
    print("Ratio Open:Close is equal to ", n , ":\t", Find_Ratio(df,"OPEN_CLOSE",n) , " times\n")
    print("Ratio Open:Low is equal to " , n , ":\t" , Find_Ratio(df,"OPEN_LOW",n) , " times\n")
    print("Ratio High:Low is equal to " , n , ":\t" , Find_Ratio(df,"HIGH_LOW",n) , " times\n")
    print("Ratio High:Close is equal to " , n , ":\t" , Find_Ratio(df,"HIGH_CLOSE",n) , " times\n")
    
#Input names of 5 stocks. Example:AAPL,AMZN,BAC,F,TSLA
s1 = input("Enter Name Of Stock: ")
s2 = input("Enter Name Of Stock: ")
s3 = input("Enter Name Of Stock: ")
s4 = input("Enter Name Of Stock: ")
s5 = input("Enter Name Of Stock: ")

df1=Create_stock(s1)
df2=Create_stock(s2)
df3=Create_stock(s3)
df4=Create_stock(s4)
df5=Create_stock(s5)

stock = {s1:df1 , s2:df2 , s3:df3 , s4:df4 , s5:df5}

for x in stock:
    print("\n \t \t \t \t \t \t",x,"\n")
    print(stock[x])
    printratio(stock[x],0.35)
    printratio(stock[x],0.5)
    printratio(stock[x],1)
    printratio(stock[x],3.5)
