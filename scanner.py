import os
import json
import time
import urllib.request
import urllib.parse

BASE = "https://api.coingecko.com/api/v3/coins/markets"

def get_page(page):
    params = urllib.parse.urlencode({
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": page,
        "sparkline": "false"
    })
    req = urllib.request.Request(
        BASE + "?" + params,
        headers={"User-Agent": "HAMSignal/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode())

def main():
    coins = []
    for page in range(1, 5):
        try:
            data = get_page(page)
            if not data:
                break
            coins.extend(data)
            print("Halaman", page, "- total koin:", len(coins))
            if page < 4:
                time.sleep(8)
        except Exception as e:
            print("Permintaan halaman", page, "gagal:", e)
            break

    coins = coins[:1000]
    print("\n=== HAM CRYPTO SCANNER ===")
    print("Jumlah koin didapat:", len(coins))
    print("Peringkat | Koin | Harga USD | Perubahan 24 jam | Volume USD")
    for c in coins:
        price = c.get("current_price")
        change = c.get("price_change_percentage_24h")
        volume = c.get("total_volume")
        print(
            str(c.get("market_cap_rank") or "-"), "|",
            c.get("symbol", "").upper(), "|",
            price if price is not None else "-", "|",
            round(change, 2) if change is not None else "-", "|",
            volume if volume is not None else "-"
        )

    try:
        with open(os.path.expanduser("~/ham-crypto-signal/market.json"), "w") as f:
            json.dump(coins, f)
        print("\nData tersimpan ke market.json")
    except Exception as e:
        print("Gagal menyimpan data:", e)

if __name__ == "__main__":
    main()
