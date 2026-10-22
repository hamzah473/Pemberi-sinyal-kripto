import json
import urllib.request
import urllib.parse
import statistics

coin = "thorchain"
q = urllib.parse.urlencode({"vs_currency":"usd","days":"7"})
url = "https://api.coingecko.com/api/v3/coins/" + coin + "/market_chart?" + q
req = urllib.request.Request(url, headers={"User-Agent":"HAMSignal/1.0"})

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())
except Exception as e:
    print("Gagal mengambil data:", e)
    raise SystemExit

prices = [x[1] for x in data.get("prices", [])]
volumes = [x[1] for x in data.get("total_volumes", [])]

def ema(values, period):
    result = values[0]
    k = 2 / (period + 1)
    for x in values[1:]:
        result = x * k + result * (1 - k)
    return result

signals = []
for i in range(24, min(len(prices), len(volumes)) - 6):
    p = prices[i]
    change6 = (p / prices[i-6] - 1) * 100
    change24 = (p / prices[i-24] - 1) * 100
    pastvol = volumes[max(0, i-24):i]
    if not pastvol:
        continue
    medianvol = statistics.median(pastvol)
    volratio = volumes[i] / medianvol if medianvol else 0
    fast = ema(prices[max(0, i-30):i+1], 9)
    slow = ema(prices[max(0, i-50):i+1], 21)

    if volratio >= 1.2 and -2 <= change6 <= 3 and change24 > -5 and fast > slow:
        future = prices[i+1:i+7]
        rise = (max(future) / p - 1) * 100
        fall = (min(future) / p - 1) * 100
        signals.append((rise, fall, change6, volratio))

print("=== HAM BACKTEST RUNE 7 HARI ===")
print("Titik harga:", len(prices))
print("Jumlah sinyal:", len(signals))
if signals:
    hits = sum(1 for x in signals if x[0] >= 5)
    print("Sinyal dengan kenaikan maksimum >=5% dalam 6 jam:", hits, "/", len(signals))
    print("Persentase hit:", round(hits / len(signals) * 100, 2), "%")
    for n, x in enumerate(signals[-10:], 1):
        print("Sinyal", n, "| potensi naik 6j:", round(x[0],2), "% | turun:", round(x[1],2), "% | volume relatif:", round(x[3],2), "x")
else:
    print("Belum ada sinyal yang memenuhi aturan.")
print("Catatan: hasil historis terbatas, belum termasuk biaya transaksi dan slippage.")
