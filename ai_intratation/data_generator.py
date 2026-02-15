import random
import pandas as pd

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
        "Auto rickshaw ride",
        "Taxi fare payment"
    ],

    "Bills": [
        "Monthly house rent",
        "Electricity bill for {month}",
        "Water bill payment",
        "Gas cylinder refill",
        "Internet bill from {isp}"
    ],

    "Health": [
        "Doctor consultation at {clinic}",
        "Medicine purchase",
        "Hospital bill payment",
        "Health checkup",
        "Pharmacy expense"
    ],

    "Shopping": [
        "Amazon shopping order",
        "Flipkart purchase",
        "Clothing shopping",
        "Electronics purchase",
        "Online shopping order",
        "Meesho online shopping"
    ],

    "Subscriptions": [
        "{service} subscription",
        "Monthly subscription for {service}",
        "{service} premium membership",
        "Auto renewal for {service}",
        "Streaming subscription payment"
    ],

    "Entertainment": [
        "Movie ticket booking",
        "Cinema ticket for {movie_type}",
        "{platform} movie rental",
        "Game purchase - {game}",
        "{platform} gaming subscription",
        "Concert ticket booking",
        "Event ticket for {event}"
    ],

    "Miscellaneous": [
        "Gift purchase",
        "Stationery items",
        "Donation payment",
        "Miscellaneous expense",
        "Unexpected expense"
    ]
}

fillers = {
    "meal": ["lunch", "dinner", "snacks"],
    "store": ["Reliance", "DMart", "Local store", "Local shop"],
    "app": ["Swiggy", "Zomato", "Blinkit", "DominosPizza", "Pizzahut", "Ovenstory"],
    "pump": ["HP", "IndianOil", "BPCL"],
    "mode": ["Bus", "Train", "Metro"],
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
              "January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"],
    "isp": ["Jio", "Airtel", "ACT", "BSNL", "Vi"],
    "clinic": ["Apollo", "Fortis", "Local clinic"],
    "service": ["Netflix", "Spotify", "Amazon Prime", "YouTube Premium"],

    # New fillers for Entertainment
    "platform": ["Netflix", "Amazon Prime", "Hotstar", "Steam", "PlayStation Store"],
    "game": ["FIFA 24", "GTA V", "Valorant skin", "PUBG UC purchase", "Minecraft"],
    "event": ["Music concert", "Stand-up comedy show", "Tech expo"],
    "movie_type": ["Bollywood movie", "Hollywood movie", "Regional film"]
}

ROWS_PER_CATEGORY = 7000
Data_set_name = "Training_data.csv"

data = []

for category, texts in templates.items():
    for _ in range(ROWS_PER_CATEGORY):
        template = random.choice(texts)
        desc = template.format(**{
            k: random.choice(v) for k, v in fillers.items()
        })
        amount = random.randint(50, 25000)
        data.append([desc, amount, category])

df = pd.DataFrame(data, columns=["description", "amount", "category"])
df.to_csv(Data_set_name, index=False)

print("Rows generated:", len(df))
print(df["category"].value_counts())