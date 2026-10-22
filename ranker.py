import json
import os

base=os.path.expanduser("~/ham-crypto-signal")
with open(base+"/market.json") as f:
    coins=json.load(f)

stable={"usdt","usdc","dai","usde","fdusd","tusd","usdp","busd","usds","usdd","usdy","usdy","eurc","eurcv","rlusd","usd1","usdg","xusd","crvusd","usdm"}
valid=[]
for c in coins:
    price=c.get("current_price")
    change=c.get("price_change_percentage_24h")
    volume=c.get("total_volume") or 0
    cap=c.get("market_cap") or 0
    rank=c.get("market_cap_rank")
    if price is None or change is None or cap<=0 or c.get("symbol","").lower() in stable:
        continue
    ratio=volume/cap
    if volume<25000 or ratio<0.02 or change < -8 or change > 12 or change < 0.2:
        continue
    score=50
    if 0 < change <= 5:
        score+=15
    elif 5 < change <= 10:
        score+=8
    elif change < -10:
        score-=15
    elif change > 10:
        score-=10
    if ratio>=0.10:
        score+=15
    elif ratio>=0.05:
        score+=10
    elif ratio<0.02:
        score-=10
    if rank and rank<=300:
        score+=5
    score=max(0,min(100,score))
    valid.append((score,c,ratio))

valid.sort(key=lambda x:x[0],reverse=True)
print("=== HAM EARLY-MOVE WATCHLIST ===")
print("Stablecoin dan pergerakan ekstrem disaring.")
print("Penyaring awal, bukan prediksi pasti.")
print("Skor | Rank | Koin | Perubahan 24j | Vol/MarketCap")
for score,c,ratio in valid[:30]:
    print(
        score,"|",c.get("market_cap_rank") or "-","|",
        c.get("symbol","").upper(),"|",
        round(c["price_change_percentage_24h"],2),"% |",
        round(ratio*100,2),"%"
    )
print("\nKandidat lolos filter:",len(valid))
print("Data sumber: snapshot CoinGecko yang tersimpan.")
