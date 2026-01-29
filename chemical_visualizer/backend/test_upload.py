import requests

url = "http://127.0.0.1:8000/api/upload/"

file = {"file": open(r"C:\Desktop\sample_equipment_data.csv", "rb")}

res = requests.post(url, files=file)

print(res.json())
