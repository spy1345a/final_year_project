import random
import pandas as pd
from datetime import datetime, timedelta

# ==================================================
# ⚙️ SETTINGS (CHANGE ONLY HERE)
# ==================================================
TOTAL_ROWS = 200          # 👈 change dataset size here
OUTPUT_FILE = "Sample_data.csv"

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)

MIN_AMOUNT = 50
MAX_AMOUNT = 25000
# ==================================================


# =========================
# Templates
# =========================
templates = {
    "Food": [
        "Swiggy food order",
        "Zomato {meal} order",
        "Restaurant {meal}",
        "Grocery shopping at {store}",
        "Food delivery via {app}"
    ],
    "Transport": [
        "Uber cab ride",
        "Fuel refill at {pump}",
        "{mode} ticket booking",
        "Auto rickshaw ride"
    ],
    "Bills": [
        "Monthly house rent",
        "Electricity bill for {month}",
        "Water bill payment",
        "Internet bill from {isp}"
    ],
    "Health": [
        "Doctor consultation at {clinic}",
        "Medicine purchase",
        "Health checkup"
    ],
    "Shopping": [
        "Amazon shopping order",
        "Flipkart purchase",
        "Clothing shopping"
    ],
    "Subscriptions": [
        "{service} subscription",
        "{service} premium membership"
    ],
    "Entertainment": [
        "Movie ticket booking",
        "{platform} movie rental",
        "Game purchase - {game}"
    ],
    "Miscellaneous": [
        "Gift purchase",
        "Donation payment",
        "Unexpected expense"
    ]
}

# =========================
# Fillers
# =========================
fillers = {
    "meal": ["lunch", "dinner", "snacks"],
    "store": ["Reliance", "DMart", "Local shop"],
    "app": ["Swiggy", "Zomato", "Blinkit"],
    "pump": ["HP", "IndianOil", "BPCL"],
    "mode": ["Bus", "Train", "Metro"],
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "isp": ["Jio", "Airtel", "ACT"],
    "clinic": ["Apollo", "Fortis", "Local clinic"],
    "service": ["Netflix", "Spotify", "Amazon Prime"],
    "platform": ["Netflix", "Hotstar", "Steam"],
    "game": ["FIFA 24", "GTA V", "Minecraft"]
}

# =========================
# Helpers
# =========================
def random_date():
    delta = END_DATE - START_DATE
    return (START_DATE + timedelta(
        days=random.randint(0, delta.days)
    )).strftime("%Y-%m-%d")


# =========================
# Data Generation
# =========================
data = []
categories = list(templates.keys())

for i in range(1, TOTAL_ROWS + 1):

    category = random.choice(categories)
    template = random.choice(templates[category])

    description = template.format(**{
        k: random.choice(v) for k, v in fillers.items()
    })

    amount = random.randint(MIN_AMOUNT, MAX_AMOUNT)
    date = random_date()

    data.append([i, description, amount, category, date])


# =========================
# Save CSV
# =========================
df = pd.DataFrame(
    data,
    columns=["ID", "Description", "Amount", "Category", "Date"]
)

df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Rows generated: {len(df)}")
print(f"✅ Saved as: {OUTPUT_FILE}")