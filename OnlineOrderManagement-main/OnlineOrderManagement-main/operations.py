from db_setup import get_connection
from models import Customer, Product, OrderItem
import mysql.connector

def add_customer(customer: Customer):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, email) VALUES (%s, %s)", (customer.name, customer.email))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        conn.close()

def add_product(product: Product):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (product_name, price, stock) VALUES (%s, %s, %s)",
                   (product.product_name, product.price, product.stock))
    conn.commit()
    conn.close()

def place_order(customer_id: int, items: list, order_date: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Validate customer
        cursor.execute("SELECT 1 FROM customers WHERE customer_id = %s", (customer_id,))
        if not cursor.fetchone():
            return "Invalid customer ID"

        # Validate products and stock
        total = 0
        for item in items:
            cursor.execute("SELECT price, stock FROM products WHERE product_id = %s", (item.product_id,))
            row = cursor.fetchone()
            if not row:
                return f"Invalid product ID: {item.product_id}"
            price, stock = row
            if item.quantity > stock:
                return f"Insufficient stock for product ID: {item.product_id}"
            total += price * item.quantity

        # Insert order
        cursor.execute("INSERT INTO orders (customer_id, order_date, total_amount) VALUES (%s, %s, %s)",
                       (customer_id, order_date, total))
        order_id = cursor.lastrowid

        # Insert order items and update stock
        for item in items:
            cursor.execute("SELECT price FROM products WHERE product_id = %s", (item.product_id,))
            price_row = cursor.fetchone()
            if not price_row or price_row[0] is None:
                conn.rollback()
                return f"Invalid price for product ID: {item.product_id}"
            price = price_row[0]
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, item_price) VALUES (%s, %s, %s, %s)",
                           (order_id, item.product_id, item.quantity, price))
            cursor.execute("UPDATE products SET stock = stock - %s WHERE product_id = %s",
                           (item.quantity, item.product_id))

        conn.commit()
        return f"Order placed successfully. Order ID: {order_id}"
    except Exception as e:
        conn.rollback()
        return f"Order failed. Transaction rolled back. Reason: {str(e)}"
    finally:
        conn.close()

def generate_invoice(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT o.order_id, o.order_date, o.total_amount, c.name, c.email
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_id = %s
    """, (order_id,))
    order = cursor.fetchone()

    cursor.execute("""
    SELECT p.product_name, oi.quantity, oi.item_price
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    WHERE oi.order_id = %s
    """, (order_id,))
    items = cursor.fetchall()
    conn.close()
    return order, items

def view_order_history(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT order_id, order_date, total_amount
    FROM orders
    WHERE customer_id = %s
    ORDER BY order_date DESC
    """, (customer_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def sales_report(start_date: str, end_date: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT order_date, SUM(total_amount)
    FROM orders
    WHERE order_date BETWEEN %s AND %s
    GROUP BY order_date
    ORDER BY order_date
    """, (start_date, end_date))
    rows = cursor.fetchall()
    conn.close()
    return rows