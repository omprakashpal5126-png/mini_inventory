import csv
import os
from datetime import datetime

# File names
PRODUCTS_FILE = "products.csv"
SALES_FILE = "sales.csv"

# ---------------- File Handling Helpers ----------------
def initialize_files():
    """Create CSV files if not exist with headers"""
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["product_id", "name", "price", "stock_quantity"])
    
    if not os.path.exists(SALES_FILE):
        with open(SALES_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["sale_id", "product_id", "quantity", "total_price", "date_time"])

# ---------------- Product Management ----------------
def add_product():
    product_id = input("Enter product ID: ")
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    stock_quantity = int(input("Enter stock quantity: "))

    with open(PRODUCTS_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([product_id, name, price, stock_quantity])
    
    print(" Product added successfully!\n")

def view_products():
    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.DictReader(f)
        print("\n--- Product List ---")
        for row in reader:
            print(f"ID: {row['product_id']} | Name: {row['name']} | Price: {row['price']} | Stock: {row['stock_quantity']}")
    print()

# ---------------- Sales Management ----------------
def sell_product():
    product_id = input("Enter product ID to sell: ")
    quantity = int(input("Enter quantity: "))
    products = []
    found = False
    sale_id = str(int(datetime.now().timestamp()))  # unique ID

    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["product_id"] == product_id:
                found = True
                stock = int(row["stock_quantity"])
                if quantity <= stock:
                    row["stock_quantity"] = str(stock - quantity)
                    total_price = float(row["price"]) * quantity
                    # Record sale
                    with open(SALES_FILE, mode="a", newline="") as sf:
                        writer = csv.writer(sf)
                        writer.writerow([sale_id, product_id, quantity, total_price, datetime.now()])
                    print(f" Sale successful! Total price: {total_price}")
                else:
                    print(" Not enough stock!")
            products.append(row)
    
    if not found:
        print(" Product not found!")

    # Update stock
    with open(PRODUCTS_FILE, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["product_id", "name", "price", "stock_quantity"])
        writer.writeheader()
        writer.writerows(products)

# ---------------- Reports ----------------
def view_sales():
    with open(SALES_FILE, mode="r") as f:
        reader = csv.DictReader(f)
        print("\n--- Sales Report ---")
        for row in reader:
            print(f"SaleID: {row['sale_id']} | ProductID: {row['product_id']} | Qty: {row['quantity']} | Total: {row['total_price']} | Date: {row['date_time']}")
    print()

def stock_report():
    view_products()

def top_selling_product():
    sales_count = {}
    with open(SALES_FILE, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["product_id"]
            qty = int(row["quantity"])
            sales_count[pid] = sales_count.get(pid, 0) + qty

    if not sales_count:
        print(" No sales yet!\n")
        return

    top_product = max(sales_count, key=sales_count.get)
    print(f" Top selling product ID: {top_product} (Sold {sales_count[top_product]} units)\n")

def daily_sales_summary():
    today = datetime.now().date()
    total_revenue = 0
    total_qty = 0

    with open(SALES_FILE, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sale_date = datetime.fromisoformat(row["date_time"]).date()
            if sale_date == today:
                total_revenue += float(row["total_price"])
                total_qty += int(row["quantity"])
    
    print("\n--- Daily Sales Summary ---")
    print(f"Total revenue today: {total_revenue}")
    print(f"Total products sold today: {total_qty}\n")

# ---------------- Menu ----------------
def menu():
    initialize_files()
    while True:
        print("==== Mini Inventory & Sales Tracker ====")
        print("1. Add Product")
        print("2. View Products")
        print("3. Sell Product")
        print("4. View Sales Report")
        print("5. Stock Report")
        print("6. Top Selling Product")
        print("7. Daily Sales Summary")
        print("0. Exit")
        
        choice = input("Enter choice: ")
        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            sell_product()
        elif choice == "4":
            view_sales()
        elif choice == "5":
            stock_report()
        elif choice == "6":
            top_selling_product()
        elif choice == "7":
            daily_sales_summary()
        elif choice == "0":
            print("👋 Exiting program. Goodbye!")
            break
        else:
            print(" Invalid choice! Try again.\n")

# ---------------- Run Program ----------------
if __name__ == "__main__":
    menu()
