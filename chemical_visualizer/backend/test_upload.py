import requests

url = "http://127.0.0.1:8000/api/upload/"

file = {
	"file": open(r"C:\Desktop\FOSSEE\chemical_visualizer\sample_equipment_data.csv", "rb")
}

res = requests.post(url, files=file, auth=("admin", "admin123"))

print(res.status_code)
print(res.json())
