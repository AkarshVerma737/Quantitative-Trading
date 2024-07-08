import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

def Create_stock(s):
    stock = yf.download(s, start="2020-01-01", end="2023-01-31",group_by='tickers')
    df = pd.DataFrame(stock)
    df = df.drop(columns=["Adj Close","Volume"])
    return df

apple=Create_stock("AAPL")
tesla=Create_stock("TSLA")

#APPLE STOCKS HIGH-LOW CANDLESTICK GRAPH
plt.figure()

w1=0.2
w2=0.02
up = apple[apple.Close >= apple.Open]
down = apple[apple.Close <= apple.Open]

c1='steelblue'
c2='black'

plt.bar(up.index,up.Close-up.Open,w1,bottom=up.Open,color=c1)
plt.bar(up.index,up.High-up.Close,w2,bottom=up.Close,color=c1)
plt.bar(up.index,up.Low-up.Open,w2,bottom=up.Open,color=c1)


plt.bar(down.index,down.Close-down.Open,w1,bottom=down.Open,color=c2)
plt.bar(down.index,down.High-down.Open,w2,bottom=down.Open,color=c2)
plt.bar(down.index,down.Low-down.Close,w2,bottom=down.Close,color=c2)

plt.xticks(rotation=45, ha = 'right')

plt.show()

#APPLE VS TESLA CLOSING PRICE

plt.plot(apple.index , apple.Close , label = "APPLE")
plt.plot(tesla.index , tesla.Close , label = "TESLA")
plt.xticks(rotation=45, ha = 'right')
plt.legend()
plt.show()
