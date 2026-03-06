import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)

FASTAPI_URL = os.getenv("FASTAPI_URL")

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