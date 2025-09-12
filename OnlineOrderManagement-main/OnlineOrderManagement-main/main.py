from db_setup import initialize_db
from models import Customer, Product, OrderItem
from operations import (
    add_customer,
    add_product,
    place_order,
    generate_invoice,
    view_order_history,
    sales_report
)

def menu():
    print("\nOnline Order Management System")
    print("1. Add Customer")
    print("2. Add Product")
    print("3. Place Order")
    print("4. Generate Invoice")
    print("5. View Order History")
    print("6. Generate Sales Report")
    print("7. Exit")

def main():
    initialize_db()
    while True:
        menu()
        choice = input("Enter your choice (1–7): ").strip()
        if choice == "1":
            name = input("Customer Name: ").strip()
            email = input("Customer Email: ").strip()
            success = add_customer(Customer(name, email))
            if success:
                print("Customer added successfully.")
            else:
                print("Customer already exists or email is duplicate.")
        elif choice == "2":
            pname = input("Product Name: ").strip()
            try:
                price = float(input("Price: "))
                stock = int(input("Stock Quantity: "))
                add_product(Product(pname, price, stock))
                print("Product added successfully.")
            except ValueError:
                print("Invalid input for price or stock.")
        elif choice == "3":
            try:
                cid = int(input("Customer ID: "))
                count = int(input("Number of items in order: "))
                items = []
                for i in range(count):
                    pid = int(input(f"Product ID for item {i+1}: "))
                    qty = int(input(f"Quantity for item {i+1}: "))
                    items.append(OrderItem(pid, qty))
                date = input("Order Date (YYYY-MM-DD): ").strip()
                result = place_order(cid, items, date)
                print(result)
            except ValueError:
                print("Invalid input. Please enter numeric values for IDs and quantities.")
        elif choice == "4":
            try:
                oid = int(input("Enter Order ID: "))
                order, items = generate_invoice(oid)
                if order:
                    print(f"\nInvoice for Order #{order[0]}")
                    print(f"Date: {order[1]}")
                    print(f"Customer: {order[3]} ({order[4]})")
                    print(f"Total Amount: ₹{order[2]:.2f}")
                    print("Items:")
                    for pname, qty, price in items:
                        print(f"  - {pname} × {qty} @ ₹{price:.2f}")
                else:
                    print("Order not found.")
            except ValueError:
                print("Invalid Order ID.")
        elif choice == "5":
            try:
                cid = int(input("Enter Customer ID: "))
                history = view_order_history(cid)
                if history:
                    print(f"\nOrder History for Customer #{cid}")
                    for oid, date, total in history:
                        print(f"  - Order #{oid} on {date} | Total: ₹{total:.2f}")
                else:
                    print("No orders found for this customer.")
            except ValueError:
                print("Invalid Customer ID.")
        elif choice == "6":
            start = input("Start Date (YYYY-MM-DD): ").strip()
            end = input("End Date (YYYY-MM-DD): ").strip()
            report = sales_report(start, end)
            if report:
                print("\nSales Report:")
                for date, total in report:
                    print(f"{date}: ₹{total:.2f}")
            else:
                print("No sales found in this date range.")
        elif choice == "7":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 7.")

if __name__ == "__main__":
    main()