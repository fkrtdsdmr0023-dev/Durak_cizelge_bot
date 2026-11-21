import json
import os
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import urllib.request
import urllib.parse

BOT_TOKEN = "AAHJBYMOVKYeCt0XbYE6q tjGdtTvsIT8AeE"
ADMIN_CHAT_ID = "8955129085"

# Plaka -> Telegram Chat ID eşleşmesi
# Sürücülerin Chat ID'lerini buraya "plaka": chat_id şeklinde ekle
SURUCULER = {
    "1392": 7575196885,
}

with open("cizelge_84_gun.json", "r", encoding="utf-8") as f:
    CIZELGE = json.load(f)

def mesaj_gonder(chat_id, metin):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": metin}).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))

def yarin_gorevlerini_dagit():
    simdi = datetime.now(ZoneInfo("Europe/Istanbul"))
    yarin_key = (simdi + timedelta(days=1)).strftime("%Y-%m-%d")
    gun_verisi = CIZELGE.get(yarin_key)
    if not gun_verisi:
        return f"Hata: {yarin_key} tarihi çizelgede bulunamadı."

    tarih_yazi = gun_verisi["tarih"]
    gorevler = gun_verisi["gorevler"]
    giden = 0
    hatalar = []

    for plaka, chat_id in SURUCULER.items():
        gorev = gorevler.get(plaka)
        if not gorev:
            continue
        mesaj = f"📅 {tarih_yazi}\n🚖 Plaka: {plaka}\n📌 Yarınki Görevin: {gorev}"
        try:
            mesaj_gonder(chat_id, mesaj)
            giden += 1
            time.sleep(0.08)
        except Exception as e:
            hatalar.append(f"{plaka}: {e}")

    ozet = f"✅ {tarih_yazi} görevleri dağıtıldı ({giden} kişiye gönderildi)."
    if hatalar:
        ozet += "\n⚠️ Gönderilemeyenler: " + ", ".join(hatalar)
    return ozet

if __name__ == "__main__":
    sonuc = yarin_gorevlerini_dagit()
    print(sonuc)
    mesaj_gonder(ADMIN_CHAT_ID, sonuc)
