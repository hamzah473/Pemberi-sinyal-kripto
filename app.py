import json
import urllib.request
import urllib.parse
import time

coins = {"BTC":"bitcoin","ETH":"ethereum","BNB":"binancecoin","SOL":"solana"}

def fetch(coin):
    q=urllib.parse.urlencode({"vs_currency":"usd","days":"1"})
    url="https://api.coingecko.com/api/v3/coins/"+coin+"/market_chart?"+q
    req=urllib.request.Request(url,headers={"User-Agent":"HAMSignal/1.0"})
    with urllib.request.urlopen(req,timeout=25) as r:
        return [x[1] for x in json.loads(r.read().decode())["prices"]]

def ema(values, period):
    k=2/(period+1)
    result=values[0]
    for x in values[1:]:
        result=x*k+result*(1-k)
    return result

def rsi(values, period=14):
    changes=[values[i]-values[i-1] for i in range(1,len(values))]
    gains=[max(x,0) for x in changes[-period:]]
    losses=[max(-x,0) for x in changes[-period:]]
    avg_gain=sum(gains)/period
    avg_loss=sum(losses)/period
    if avg_loss==0:
        return 100 if avg_gain>0 else 50
    return 100-(100/(1+avg_gain/avg_loss))

def main():
    print("=== HAM CRYPTO SIGNAL ===")
    for symbol,coin in coins.items():
        try:
            time.sleep(3)
            prices=fetch(coin)
            if len(prices)<30:
                print(symbol+": Data belum cukup")
                continue
            price=prices[-1]
            fast=ema(prices[-20:],9)
            slow=ema(prices[-26:],21)
            strength=rsi(prices)
            if strength<30 and fast>slow:
                signal="BUY"
            elif strength>70 and fast<slow:
                signal="SELL"
            else:
                signal="WAIT"
            print("\n"+symbol+"/USD")
            print("Harga:",round(price,4))
            print("RSI:",round(strength,2))
            print("EMA 9:",round(fast,4))
            print("EMA 21:",round(slow,4))
            print("Sinyal:",signal)
        except Exception as e:
            print(symbol,"gagal:",e)

if __name__=="__main__":
    main()
