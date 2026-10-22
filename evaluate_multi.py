import json, os

base = os.path.expanduser("~/ham-crypto-signal")
data = json.load(open(os.path.join(base,"history_cache.json")))
print("=== HAM SIGNAL: UJI 9 KOIN ===")
print("Koin | Sinyal | Naik >=5% | Turun <=-5% | Kenaikan % | Penurunan %")
total_signals = total_pumps = total_dumps = 0

for coin_id, d in data.items():
    prices, volumes = d["prices"], d["volumes"]
    signals = []
    for i in range(24, min(len(prices),len(volumes))-6):
        past = volumes[i-24:i]
        avg = sum(past)/len(past)
        ratio = volumes[i]/avg if avg else 0
        change6 = (prices[i]/prices[i-6]-1)*100
        change24 = (prices[i]/prices[i-24]-1)*100
        if ratio >= 1.5 and abs(change6) <= 3 and change24 > -5:
            future = prices[i+1:i+7]
            up = (max(future)/prices[i]-1)*100
            down = (min(future)/prices[i]-1)*100
            signals.append((up,down))
    pumps = sum(1 for x in signals if x[0] >= 5)
    dumps = sum(1 for x in signals if x[1] <= -5)
    n = len(signals)
    total_signals += n
    total_pumps += pumps
    total_dumps += dumps
    print(d["symbol"],"|",n,"|",pumps,"|",dumps,"|",round(pumps/n*100,1) if n else 0,"% |",round(dumps/n*100,1) if n else 0,"%")

print("TOTAL |",total_signals,"|",total_pumps,"|",total_dumps)
print("Catatan: jendela tujuh hari, data per jam, dan sinyal yang berdekatan dapat tumpang tindih. Ini bukan bukti kemampuan prediksi.")
