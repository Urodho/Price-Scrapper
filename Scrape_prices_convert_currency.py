import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


url = "https://books.toscrape.com/"


response = requests.get(url)

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find all the book products
books = soup.find_all("article",
class_="product_pod")

#  Create empty lists
book_names =[]
book_prices =[]

# Get the first 10 books
for book in books[:10]:
    title = book.h3.a["title"]
    price = book.find("p",
                       class_="price_color").text

    book_names.append(title)
    book_prices.append(price)

    # Create a table
data = pd.DataFrame({
    "Book Name": book_names,
    "Price": book_prices
    })

# Display the table
print(data)

# Sav to CSV
data.to_csv("books.csv", index=False)

print("Data saved successfully as books.csv")

response = requests.get("https://open.er-api.com/v6/latest/GBP")

rate = response.json()["rates"]["KES"]


converted_prices = []
for price in book_prices:
    import re
    amount = float(re.sub(r"[^\d.]","", price))

    # Convert GBP to KES
    kes = amount * rate

    converted_prices.append(round(kes, 2))

# Create a table
data = pd.DataFrame({
    "Book Name": book_names,
    "Prices(GBP)": book_prices,
    "Price(KES)": converted_prices
})    

# Display the table
print(data)

data.to_csv("books.csv", index=False)

print("Data saved succesfully as books.csv")

# Add a timestamp

print("Conversion Date and Time ")
print(datetime.now())

# Plot for bar chart

plt.figure(figsize=(10,5))
plt.bar(book_names, converted_prices)
plt.xticks(rotation=90)
plt.title(f"Book Price in KES")
plt.xlabel("Books")
plt.ylabel(f"Prices (KES)")
plt.tight_layout()
plt.show()