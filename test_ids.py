import xml.etree.ElementTree as ET
from collections import Counter

tree = ET.parse('huge_map.drawio')
root = tree.getroot()
ids = []
for elem in root.iter():
    if 'id' in elem.attrib:
        ids.append(elem.attrib['id'])

counter = Counter(ids)
for id, count in counter.items():
    if count > 1:
        print(f"Duplicate ID: {id} ({count} times)")
