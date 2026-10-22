import json, urllib.request, urllib.parse

coin = "thorchain"
q = urllib.parse.urlencode({"vs_currency":"usd","days":"7"})
url = "https://api.coingecko.com/api/v3/coins/" + coin + "/market_chart?" + q
req = urllib.request.Request(url, headers={"User-Agent":"HAMSignal/1.0"})

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read().decode())
except Exception as e:
    print("Gagal mengambil data:", e)
    raise SystemExit

prices = [x[1] for x in d.get("prices", [])]
volumes = [x[1] for x in d.get("total_volumes", [])]
if len(prices) < 32 or len(volumes) != len(prices):
    print("Data historis tidak cukup.")
    raise SystemExit

events = []
for i in range(24, len(prices)-6):
    past = volumes[i-24:i]
    avg = sum(past)/len(past)
    ratio = volumes[i]/avg if avg else 0
    move6 = (prices[i]/prices[i-6]-1)*100
    if ratio >= 1.5 and abs(move6) <= 3:
        future = prices[i+1:i+7]
        up = (max(future)/prices[i]-1)*100
        down = (min(future)/prices[i]-1)*100
        events.append((up, down, ratio))

pump = sum(1 for x in events if x[0] >= 5)
dump = sum(1 for x in events if x[1] <= -5)
print("=== HAM PUMP/DUMP TEST ===")
print("Koin: RUNE | Data:",len(prices),"titik per jam")
print("Peringatan volume meningkat:",len(events))
print("Peringatan diikuti kenaikan >=5%:",pump)
print("Peringatan diikuti penurunan >=5%:",dump)
if events:
    print("Persentase kenaikan:",round(pump/len(events)*100,2),"%")
    print("Persentase penurunan:",round(dump/len(events)*100,2),"%")
else:
    print("Belum ada kejadian yang memenuhi aturan.")
print("Catatan: satu koin dan tujuh hari bukan bukti akurasi masa depan.")
