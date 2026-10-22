import json
import os

base=os.path.expanduser("~/ham-crypto-signal")
with open(base+"/market.json") as f:
    coins=json.load(f)

stable={"usdt","usdc","dai","usde","fdusd","tusd","usdp","busd","usds","usdd","usdy","eurc","eurcv","rlusd","usd1","usdg","xusd","crvusd","usdm"}
rows=[]

for c in coins:
    symbol=c.get("symbol","").lower()
    price=c.get("current_price")
    change=c.get("price_change_percentage_24h")
    volume=c.get("total_volume") or 0
    cap=c.get("market_cap") or 0
    rank=c.get("market_cap_rank")
    if symbol in stable or price is None or change is None or cap<=0:
        continue
    ratio=volume/cap
    if volume<25000 or ratio<0.02 or change<0.2 or change>12 or change < -8:
        continue
    score=50
    if change<=3:
        score+=15
    elif change<=5:
        score+=8
    if ratio>=0.10:
        score+=15
    elif ratio>=0.05:
        score+=10
    if rank and rank<=300:
        score+=5
    rows.append({
        "rank":rank,"symbol":symbol.upper(),"name":c.get("name"),
        "price_usd":price,"market_cap_usd":cap,
        "volume_usd":volume,"change_24h_pct":change,
        "volume_to_market_cap_pct":ratio*100,"screen_score":min(score,100)
    })

rows.sort(key=lambda x:x["screen_score"],reverse=True)
with open(base+"/candidates.json","w") as f:
    json.dump(rows,f,indent=2)

print("=== HAM CRYPTO SIGNAL: LAPORAN KANDIDAT ===")
print("Jumlah kandidat:",len(rows))
print("Skor adalah skor filter, bukan probabilitas kenaikan.")
for x in rows[:20]:
    print("\n",x["symbol"],"-",x["name"],"| Rank:",x["rank"])
    print("Harga USD:",x["price_usd"],"| Perubahan 24j:",round(x["change_24h_pct"],2),"%")
    print("Market cap USD:",round(x["market_cap_usd"]))
    print("Volume USD:",round(x["volume_usd"]))
    print("Volume/market cap:",round(x["volume_to_market_cap_pct"],2),"%")
    print("Skor filter:",x["screen_score"])
print("\nLaporan tersimpan di candidates.json")
