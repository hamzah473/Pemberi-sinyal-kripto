import json, os, time, urllib.request, urllib.parse

base=os.path.expanduser("~/ham-crypto-signal")
all_coins=[]
for page in range(1,5):
    params=urllib.parse.urlencode({
        "vs_currency":"usd",
        "order":"market_cap_desc",
        "per_page":250,
        "page":page,
        "sparkline":"false",
        "price_change_percentage":"24h"
    })
    url="https://api.coingecko.com/api/v3/coins/markets?"+params
    req=urllib.request.Request(url,headers={"User-Agent":"HAMSignal/1.0"})
    try:
        with urllib.request.urlopen(req,timeout=30) as r:
            batch=json.loads(r.read().decode())
        all_coins.extend(batch)
        print("Halaman",page,"berhasil:",len(batch),"koin")
    except Exception as e:
        print("Gagal halaman",page,":",e)
        break
    if page<4:
        time.sleep(8)

if not all_coins:
    print("Tidak ada data baru. File lama tidak diubah.")
    raise SystemExit

with open(base+"/market.json","w") as f:
    json.dump(all_coins,f)
print("Data pasar diperbarui:",len(all_coins),"koin")
