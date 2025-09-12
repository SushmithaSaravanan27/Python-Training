import pytest
from db_setup import initialize_db, reset_tables, get_connection
from models import Customer, Product, OrderItem
from operations import (
    add_customer,
    add_product,
    place_order,
    generate_invoice,
    view_order_history,
    sales_report
)

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    initialize_db()

@pytest.fixture(autouse=True)
def clean_db():
    reset_tables()

# ------------------ Customer Tests ------------------

def test_add_customer_success():
    assert add_customer(Customer("Alice", "alice@example.com")) is True

def test_add_customer_duplicate_email():
    add_customer(Customer("Bob", "bob@example.com"))
    assert add_customer(Customer("Bob", "bob@example.com")) is False

# ------------------ Product Tests ------------------

def test_add_product_success():
    add_product(Product("Laptop", 50000.0, 10))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE product_name = %s", ("Laptop",))
    assert cursor.fetchone() is not None
    conn.close()

# ------------------ Order Placement ------------------

def test_place_order_success():
    add_customer(Customer("Carol", "carol@example.com"))
    add_product(Product("Mouse", 500.0, 5))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM customers WHERE email = %s", ("carol@example.com",))
    cid = cursor.fetchone()[0]
    cursor.execute("SELECT product_id FROM products WHERE product_name = %s", ("Mouse",))
    pid = cursor.fetchone()[0]
    conn.close()

    result = place_order(cid, [OrderItem(pid, 2)], "2025-09-11")
    assert "Order placed successfully" in result

def test_place_order_insufficient_stock():
    add_customer(Customer("Dave", "dave@example.com"))
    add_product(Product("Keyboard", 1000.0, 1))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM customers WHERE email = %s", ("dave@example.com",))
    cid = cursor.fetchone()[0]
    cursor.execute("SELECT product_id FROM products WHERE product_name = %s", ("Keyboard",))
    pid = cursor.fetchone()[0]
    conn.close()

    result = place_order(cid, [OrderItem(pid, 5)], "2025-09-11")
    assert result == "Insufficient stock for product ID: {}".format(pid)

# ------------------ Invoice ------------------

def test_generate_invoice_contents():
    add_customer(Customer("Eve", "eve@example.com"))
    add_product(Product("Monitor", 15000.0, 5))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM customers WHERE email = %s", ("eve@example.com",))
    cid = cursor.fetchone()[0]
    cursor.execute("SELECT product_id FROM products WHERE product_name = %s", ("Monitor",))
    pid = cursor.fetchone()[0]
    conn.close()

    result = place_order(cid, [OrderItem(pid, 2)], "2025-09-11")
    assert "Order placed successfully" in result

    order_id = int(result.split(":")[1].strip())
    order, items = generate_invoice(order_id)
    assert order is not None
    assert len(items) == 1
    assert items[0][0] == "Monitor"

# ------------------ Order History ------------------

def test_view_order_history_contains_order():
    add_customer(Customer("Frank", "frank@example.com"))
    add_product(Product("Headphones", 3000.0, 5))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM customers WHERE email = %s", ("frank@example.com",))
    cid = cursor.fetchone()[0]
    cursor.execute("SELECT product_id FROM products WHERE product_name = %s", ("Headphones",))
    pid = cursor.fetchone()[0]
    conn.close()

    result = place_order(cid, [OrderItem(pid, 1)], "2025-09-11")
    assert "Order placed successfully" in result

    history = view_order_history(cid)
    assert len(history) >= 1
    assert history[0][2] >= 3000.0

# ------------------ Sales Report ------------------

def test_sales_report_includes_order_date():
    add_customer(Customer("Grace", "grace@example.com"))
    add_product(Product("Webcam", 2500.0, 5))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM customers WHERE email = %s", ("grace@example.com",))
    cid = cursor.fetchone()[0]
    cursor.execute("SELECT product_id FROM products WHERE product_name = %s", ("Webcam",))
    pid = cursor.fetchone()[0]
    conn.close()

    result = place_order(cid, [OrderItem(pid, 2)], "2025-09-11")
    assert "Order placed successfully" in result

    report = sales_report("2025-09-10", "2025-09-12")
    assert any(str(row[0]) == "2025-09-11" for row in report)

def test_sales_report_total_amount_correct():
    add_customer(Customer("Hank", "hank@example.com"))
    add_product(Product("Webcam", 2500.0, 5))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM customers WHERE email = %s", ("hank@example.com",))
    cid = cursor.fetchone()[0]
    cursor.execute("SELECT product_id FROM products WHERE product_name = %s", ("Webcam",))
    pid = cursor.fetchone()[0]
    conn.close()

    result = place_order(cid, [OrderItem(pid, 2)], "2025-09-11")
    assert "Order placed successfully" in result

    report = sales_report("2025-09-10", "2025-09-12")
    total = sum(row[1] for row in report)
    assert total >= 5000.0