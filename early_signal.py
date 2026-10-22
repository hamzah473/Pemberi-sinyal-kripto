import json, os

base=os.path.expanduser("~/ham-crypto-signal")
with open(base+"/market.json") as f:
    coins=json.load(f)

stable={"usdt","usdc","dai","usde","fdusd","tusd","usdp","busd","usds","usdd","usdy","eurc","eurcv","rlusd","usd1","usdg","xusd","crvusd","usdm"}
results=[]

for c in coins:
    price=c.get("current_price")
    change=c.get("price_change_percentage_24h")
    volume=c.get("total_volume") or 0
    cap=c.get("market_cap") or 0
    rank=c.get("market_cap_rank")
    symbol=c.get("symbol","").lower()

    if price is None or change is None or cap<=0 or symbol in stable:
        continue
    if volume<25000:
        continue

    ratio=volume/cap
    if ratio<0.02 or not (-5<=change<=5):
        continue

    score=50
    reasons=[]

    if 0.2<=change<=3:
        score+=15
        reasons.append("harga naik ringan")
    elif -2<=change<0.2:
        score+=10
        reasons.append("harga masih dekat area datar")
    elif change < -2:
        reasons.append("harga sedang melemah")

    if ratio>=0.20:
        score+=20
        reasons.append("volume relatif tinggi")
    elif ratio>=0.10:
        score+=15
        reasons.append("volume meningkat relatif")
    elif ratio>=0.05:
        score+=8
        reasons.append("volume cukup")

    if rank and rank<=300:
        score+=5
        reasons.append("peringkat pasar relatif tinggi")

    results.append({
        "score":min(score,100),
        "rank":rank or 999999,
        "symbol":symbol.upper(),
        "name":c.get("name"),
        "price":price,
        "change24h":change,
        "volume":volume,
        "volume_marketcap_pct":ratio*100,
        "reasons":", ".join(reasons)
    })

results.sort(key=lambda x:(-x["score"],x["rank"]))
out=base+"/early_signals.json"
with open(out,"w") as f:
    json.dump(results,f,indent=2)

print("=== HAM EARLY SIGNAL ===")
print("Koin terpilih:",len(results))
print("Skor adalah skor penyaringan, bukan probabilitas pump.")
print("Skor | Rank | Koin | Perubahan 24j | Vol/MarketCap | Alasan")
for x in results[:25]:
    print(x["score"],"|",x["rank"],"|",x["symbol"],"|",round(x["change24h"],2),"% |",round(x["volume_marketcap_pct"],2),"% |",x["reasons"])
print("Disimpan:",out)
print("Peringatan: data snapshot, belum menguji urutan harga dan volume intrahari.")
