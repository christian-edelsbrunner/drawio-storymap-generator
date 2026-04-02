import yaml
with open('huge_map.yaml') as f:
    data = yaml.safe_load(f)
maps = data.get('maps', [])
print(f"Number of maps: {len(maps)}")
for m in maps:
    print(f"Map: {m['id']}")
