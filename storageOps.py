import sqlite3

from Provider import Provider
from constants import DB_NAME
from crypto import encrypt_password
import datetime
from prettytable import *
from Product import ProductInOrder


def create_user(login, password, firstname, lastname, address, telephone, date_of_birth):
    try:
        encrypted_password = encrypt_password(password)
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        string_to_execute = "INSERT INTO User (email, password, firstname," \
                            "lastname, address, telephone, date_of_birth) values (" \
                            + "'" + login + "'" + "," + "'" + encrypted_password + "'" + "," \
                            + "'" + firstname + "'" + "," + "'" + lastname + "'" + "," + "'" \
                            + address + "'" + "," + "'" + telephone + "'" + "," + "'" + date_of_birth + "'" ");"
        cursor.execute(string_to_execute)
        cursor.execute("COMMIT;")
        cursor.close()
        connection.close()
    except BaseException as err:
        print(err)


def validate_login_details(login, password):
    try:
        encrypted_password = encrypt_password(password)
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        string_to_execute = "SELECT user_id, password" + " FROM User WHERE email = " + "'" + login + "'" \
                            + " AND password = " + "'" + encrypted_password + "'" + ";"
        cursor.execute(string_to_execute)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result is not None:
            return result[0]
        else:
            return False
    except BaseException as err:
        print(err)


def view_product_catalog(category_id):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        string_to_execute = "SELECT product_id, name, unitprice, category_id FROM Product WHERE category_id = " + str(
            category_id) + ";"
        cursor.execute(string_to_execute)
        result = cursor.fetchall()
        print("")
        product_table = PrettyTable()
        product_table.field_names = ['Product ID', 'Name', 'Unit Price', 'Category ID']
        for r in result:
            product_table.add_row([r[0], r[1], r[2], r[3]])
        print(product_table)
        cursor.close()
        connection.close()
    except BaseException as err:
        print(err)


def view_categories(category_id):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        string_to_execute = "SELECT name, category_id FROM ProductCategory WHERE parent_category_id = " + str(
            category_id) + \
                            " AND category_id!= parent_category_id" + ";" \
            if category_id is not None else "SELECT name, category_id FROM ProductCategory WHERE category_id = parent_category_id;"
        cursor.execute(string_to_execute)
        result = cursor.fetchall()
        if len(result) == 0:
            string_to_execute = "SELECT * FROM ProductCategory WHERE category_id = " + str(category_id) + ";"
            cursor.execute(string_to_execute)
            result = cursor.fetchall()
            if len(result) == 0:
                cursor.close()
                connection.close()
                return False
            else:
                view_product_catalog(category_id)
                return True
        print("")
        category_table = PrettyTable()
        category_table.field_names = ['ID', 'Category']
        for r in result:
            category_table.add_row([r[1], r[0]])
        print(category_table)
        cursor.close()
        connection.close()
    except BaseException as err:
        print(err)


def create_order(products, user_id, payment_id):
    try:
        order_date = datetime.date.today().strftime("%d-%m-%Y")
        total = 0
        for product in products:
            total += product.unitprice * product.quantity

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        string_to_execute = "INSERT INTO OrderDetails values (" \
                            + "null," + str(user_id) + "," + "'" + order_date + "'" + "," \
                            + str(total) + "," + str(payment_id) \
                            + ");"
        cursor.execute(string_to_execute)

        order_id = cursor.lastrowid
        cursor.execute("COMMIT;")
        for product in products:
            string_to_execute = "INSERT INTO OrderItems values (" \
                                + "null," + str(order_id) + "," + str(product.product_id) + "," \
                                + str(product.quantity) + ");"
            cursor.execute(string_to_execute)

            cursor.execute("COMMIT;")
        cursor.close()
        connection.close()
        return order_id
    except BaseException as err:
        print(err)


def view_orders(user_id):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        string_to_execute = "SELECT order_id, order_date, total, payment_id " \
                            "FROM OrderDetails WHERE user_id = " + str(user_id) + ";"
        cursor.execute(string_to_execute)

        result = cursor.fetchall()
        cursor.close()
        connection.close()
        print("")
        order_table = PrettyTable()
        order_table.field_names = ['Order ID', 'Order Date', 'Total', 'Payment ID']
        for r in result:
            order_table.add_row([r[0], r[1], r[2], r[3]])
        print(order_table)
    except BaseException as err:
        print(err)


def view_cart(user_id):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        string_to_execute = "SELECT user_id, product_id, quantity, product_name " \
                            "FROM CartItems WHERE user_id = " + str(user_id) + ";"
        cursor.execute(string_to_execute)

        result = cursor.fetchall()
        cursor.close()
        connection.close()
        print("")
        cart_table = PrettyTable()
        cart_table.field_names = ['User ID', 'Product ID', 'Product Name', 'Quantity']
        for r in result:
            cart_table.add_row([r[0], r[1], r[3], r[2]])
        print(cart_table)
    except BaseException as err:
        print(err)


def add_to_cart(user_id, products):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        for product in products:
            string_to_execute = "SELECT name, unitprice FROM Product WHERE product_id = " + str(
                product.product_id) + ";"
            cursor.execute(string_to_execute)

            result = cursor.fetchall()
            product.name = result[0][0]
            product.unitprice = result[0][1]
            string_to_execute = "INSERT INTO CartItems values (" \
                                + "null," + str(user_id) + "," + str(product.product_id) + "," \
                                + str(product.quantity) + "," + "'" + product.name + "'" + "," + str(
                product.unitprice) + ");"
            cursor.execute(string_to_execute)
            cursor.execute("COMMIT;")
        cursor.close()
        connection.close()
    except BaseException as err:
        print(err)


def check_cart_items(user_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    string_to_execute = "SELECT * " \
                        "FROM CartItems WHERE user_id = " + str(user_id) + ";"
    cursor.execute(string_to_execute)

    result = cursor.fetchall()
    if len(result) == 0:
        return False
    else:
        return True


def checkout_cart_items(user_id, payment_id):
    try:
        check = check_cart_items(user_id)
        if check == False:
            print("Empty cart, cannot checkout!")
            return
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        string_to_execute = "SELECT product_id, quantity, unitprice, product_name " \
                            "FROM CartItems WHERE user_id = " + str(user_id) + ";"
        cursor.execute(string_to_execute)

        result = cursor.fetchall()
        products = []
        total = 0
        for r in result:
            total += r[2]
            products.append(ProductInOrder(r[0], r[1], r[2], r[3]))
        order_id = create_order(products, user_id, payment_id)
        checkout(order_id, total, Provider(payment_id).name, "Recieved")
        string_to_execute = "DELETE FROM CartItems  WHERE user_id = " + str(user_id) + ";"
        cursor.execute(string_to_execute)

        cursor.execute("COMMIT;")
        cursor.close()
        connection.close()
    except BaseException as err:
        print(err)


def checkout(order_id, amount, provider, status):
    try:
        payment_date = datetime.date.today().strftime("%d-%m-%Y")
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        string_to_execute = "INSERT INTO PaymentDetails values (" \
                            + "null," + str(order_id) + "," + str(amount) + "," \
                            + "'" + provider + "'" + "," + "'" + status + "'" + "," \
                            + "'" + payment_date + "'" + ");"
        cursor.execute(string_to_execute)

        cursor.execute("COMMIT;")
        cursor.close()
        connection.close()
    except BaseException as err:
        print(err)

