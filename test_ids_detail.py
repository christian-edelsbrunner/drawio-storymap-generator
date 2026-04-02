import xml.etree.ElementTree as ET

tree = ET.parse('huge_map.drawio')
root = tree.getroot()
for elem in root.iter():
    if elem.attrib.get('id') == 'goal_GOAL-1':
        print(f"Tag: {elem.tag}")
        print(f"Attribs: {elem.attrib}")
        print(f"Parent: {elem.get('parent', 'unknown')}")
        print("---")
