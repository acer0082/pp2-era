import json

# читаем файл
with open("sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)

print(f"{'DN':50} {'Description':20} {'Speed':8} {'MTU':6}")
print("-" * 80)

# перебираем интерфейсы
for item in data["imdata"]:
    attr = item["l1PhysIf"]["attributes"]
    
    dn = attr.get("dn", "")
    descr = attr.get("descr", "")
    speed = attr.get("speed", "")
    mtu = attr.get("mtu", "")
    
    print(f"{dn:50} {descr:20} {speed:8} {mtu:6}")