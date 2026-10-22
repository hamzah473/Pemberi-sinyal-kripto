import json, os

base=os.path.expanduser("~/ham-crypto-signal")
data=json.load(open(base+"/early_signals.json")) if os.path.exists(base+"/early_signals.json") else []
print("=== HAM CRYPTO SIGNAL ===")
print("Catatan: label ini indikasi awal, bukan kepastian arah harga.")
print("\n--- POTENSI NAIK: momentum positif ---")
up=[x for x in data if x["change24h"]>0]
for x in up[:15]:
    print(x["symbol"],"| skor",x["score"],"| perubahan",round(x["change24h"],2),"% | volume/kapitalisasi",round(x["volume_marketcap_pct"],2),"%")
print("\n--- POTENSI TURUN: momentum negatif ---")
down=[x for x in data if x["change24h"]<0]
down.sort(key=lambda x:x["change24h"])
for x in down[:15]:
    print(x["symbol"],"| skor",x["score"],"| perubahan",round(x["change24h"],2),"% | volume/kapitalisasi",round(x["volume_marketcap_pct"],2),"%")
print("\nJumlah kandidat:",len(data))
print("Peringatan: perubahan 24 jam tidak membuktikan arah berikutnya.")
