import requests

FASTAPI_URL = "http://127.0.0.1:9111"

files = {
    "file": open("Sample_data.csv", "rb")
}

headers = {
    "admin-key": "supersecretkey123"
}

r = requests.post(
    f"{FASTAPI_URL}/expenses/import-default",
    files=files,
    headers=headers
)

print(r.json())