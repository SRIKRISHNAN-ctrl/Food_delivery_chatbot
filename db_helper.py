import mysql.connector

def get_order_status(order_id: int):
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pandeyji_eatery"
    )
    try:
        cursor = cnx.cursor()
        query = "SELECT status FROM order_tracking WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        return result
    finally:
        cnx.close()

def get_next_order_id():
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pandeyji_eatery"
    )
    try:
        cursor = cnx.cursor()
        query = "SELECT MAX(order_id) FROM orders"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        if result is None:
            return 1
        else:
            return result + 1
    finally:
        cnx.close()

def get_total_order_price(order_id):
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pandeyji_eatery"
    )
    try:
        cursor = cnx.cursor()
        query = f"SELECT get_total_order_price({order_id})"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result
    finally:
        cnx.close()

def insert_order_tracking(order_id, status):
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pandeyji_eatery"
    )
    try:
        cursor = cnx.cursor()
        insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
        cursor.execute(insert_query, (order_id, status))
        cnx.commit()
    finally:
        cnx.close()

# Function to call the MySQL stored procedure and insert an order item
def insert_order_item(food_item, quantity, order_id):
    try:
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="pandeyji_eatery"
        )
        cursor = cnx.cursor()
        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))
        # Executing the stored procedure
        cursor.execute("SELECT @_insert_order_item_0, @_insert_order_item_1, @_insert_order_item_2")
        # Fetching the output parameters
        result = cursor.fetchone()
        # Committing the changes
        cnx.commit()
        print("Order item inserted successfully!")
        return result
    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")
        # Rollback changes if necessary
        cnx.rollback()
    finally:
        cnx.close()
