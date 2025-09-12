import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ecom"
    )

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL,
        price FLOAT NOT NULL,
        stock INT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        order_date DATE,
        total_amount FLOAT,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        item_id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        product_id INT,
        quantity INT,
        item_price FLOAT,
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    )
    """)

    conn.commit()
    conn.close()

def reset_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM order_items")
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM customers")
    conn.commit()
    conn.close()