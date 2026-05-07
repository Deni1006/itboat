import json
import os

files = [f for f in os.listdir('.') if f.startswith('raw_') and f.endswith('.json')]
if not files:
    print("JSON файл не найден")
    exit()

latest_file = sorted(files)[-1]
print(f"Файл: {latest_file}")

with open(latest_file, 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Всего записей: {len(items)}")

unique_ids = set()
for item in items:
    unique_ids.add(item['id'])

print(f"Уникальных объявлений: {len(unique_ids)}")

if len(items) > len(unique_ids):
    print(f"Дубликатов: {len(items) - len(unique_ids)}")

if items:
    print(f"\nДоступные поля в объявлении:")
    for key in items[0].keys():
        print(f"  - {key}")