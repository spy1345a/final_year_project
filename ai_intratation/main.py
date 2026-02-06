from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "household_expenses.csv"

df = pd.read_csv(csv_path)

print(df.head())

