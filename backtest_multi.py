import json, os, time, urllib.request, urllib.parse

base = os.path.expanduser("~/ham-crypto-signal")
coins = [
    ("RUNE","THORChain","thorchain"),
    ("ZAMA","Zama","zama"),
    ("GOMINING","GoMining Token","gmt-token"),
    ("ATH","Aethir","aethir"),
    ("GRASS","Grass","grass"),
    ("SENT","Sentient","sentient"),
    ("BEAM","Beam","beam-2"),
    ("EDGE","edgeX","edgex"),
    ("CAP","Cap","cap-4"),
    ("BAN","Comedian","comedian")
]
cache = os.path.join(base, "history_cache.json")
try:
    all_data = json.load(open(cache))
except Exception:
    all_data = {}

for symbol, name, coin_id in coins:
    if coin_id in all_data:
        print(symbol, "data cache tersedia")
        continue
    q = urllib.parse.urlencode({"vs_currency":"usd","days":"7"})
    url = "https://api.coingecko.com/api/v3/coins/" + coin_id + "/market_chart?" + q
    req = urllib.request.Request(url, headers={"User-Agent":"HAMSignal/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode())
        prices = [x[1] for x in d.get("prices", [])]
        volumes = [x[1] for x in d.get("total_volumes", [])]
        if len(prices) > 30 and len(prices) == len(volumes):
            all_data[coin_id] = {"symbol":symbol,"name":name,"prices":prices,"volumes":volumes}
            with open(cache,"w") as f:
                json.dump(all_data,f)
            print(symbol, "OK:",len(prices),"titik")
        else:
            print(symbol, "data tidak cukup")
    except Exception as e:
        print(symbol, "gagal:",str(e))
    time.sleep(8)

print("Total koin tersimpan:",len(all_data))
print("File cache:",cache)
