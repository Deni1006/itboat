import json
import os
from datetime import datetime
from clickhouse_driver import Client


def normalize():
    client = Client(
        host='clickhouse',
        port=9000,
        user='click',
        password='click'
    )

    raw_files = sorted([f for f in os.listdir('raw_data') if f.startswith('raw_') and f.endswith('.json')])
    latest_file = os.path.join('raw_data', raw_files[-1])

    with open(latest_file, 'r', encoding='utf-8') as f:
        items = json.load(f)

    print(f"Загружено {len(items)} объявлений из {latest_file}")

    for item in items:
        price_val = item.get('price')
        price_val = float(price_val) if price_val is not None else 0.0

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


if __name__ == "__main__":
    normalize()
