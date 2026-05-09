from apify_client import ApifyClient
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_TOKEN")

client = ApifyClient(APIFY_TOKEN)

run_input = {
    "searchUrl": "https://www.avito.ru/all/vodnyy_transport/katera_i_yahty-ASgBAgICAUQOPg?cd=1&context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6InkiO3M6MTY6IklGaVlmaDE1WXFNMVZpdXIiO31PZmggJgAAAA&q=%D1%8F%D1%85%D1%82%D0%B0",
    "maxResults": 20,
}

print("Запуск zen-studio/avito-listings-scraper...")
run = client.actor("zen-studio/avito-listings-scraper").call(run_input=run_input)

print("Получение результатов...")
items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

filename = f"raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Сохранено {len(items)} объявлений в {filename}")

if items:
    print("\nСтруктура первого объявления:")
    first = items[0]
    for key in first.keys():
        print(f"  {key}: {type(first[key]).__name__}")