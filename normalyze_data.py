import json
from datetime import datetime
from clickhouse_driver import Client

client = Client(
    host='localhost',
    port=9002,
    user='click',
    password='click'
)

client.execute("""
    CREATE TABLE IF NOT EXISTS yacht_listings (
        id UInt64,
        title String,
        price Float64,
        currency String,
        url String,
        images String,
        source String,
        collected_at DateTime
    ) ENGINE = MergeTree()
    ORDER BY collected_at
""")

print("Таблица готова")

with open('raw_20260428_132631.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Загружено {len(items)} объявлений")

for item in items:
    price_val = item.get('price')
    if price_val is None:
        price_val = 0
    else:
        price_val = float(price_val)
    
    images_json = json.dumps(item.get("images", []))
    
    client.execute("""
        INSERT INTO yacht_listings (id, title, price, currency, url, images, source, collected_at)
        VALUES (%(id)s, %(title)s, %(price)s, %(currency)s, %(url)s, %(images)s, %(source)s, %(collected_at)s)
    """, {
        "id": item["id"],
        "title": item["title"],
        "price": price_val,
        "currency": item.get("currency", "RUB"),
        "url": item["url"],
        "images": images_json,
        "source": "avito",
        "collected_at": datetime.now()
    })

print(f"Данные загружены. Всего: {len(items)} записей")

result = client.execute("SELECT COUNT(*) FROM yacht_listings")
print(f"В таблице {result[0][0]} записей")