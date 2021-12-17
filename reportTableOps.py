import sqlite3
import pandas as pd
import os
from constants import DB_NAME
from prettytable import *

def reportGenerator():
    conn = sqlite3.connect('User.db')
    directory = "./data"
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".csv")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)

        os.remove(path_to_file)
    c = conn.cursor()
    for table in c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
        t = table[0]
        df = pd.read_sql('SELECT * from ' + t, conn)
        df.to_csv(os.path.join(directory,t + '.csv'))

def showBestSellingCategories():
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        string_to_execute = "select PCGrandParent.name, COUNT(PCGrandParent.name) " \
                            "from OrderItems inner join OrderDetails OD on OrderItems.order_id = OD.order_id " \
                            "inner join Product P on OrderItems.product_id = P.product_id " \
                            "inner join ProductCategory PC on P.category_id = PC.category_id " \
                            "inner join ProductCategory PCParent on PCParent.category_id = PC.parent_category_id " \
                            "inner join ProductCategory PCGrandParent on PCGrandParent.category_id = PCParent.parent_category_id " \
                            "GROUP BY PCGrandParent.name ORDER BY 2 DESC";
        cursor.execute(string_to_execute)
        result = cursor.fetchall()
        print("")
        product_table = PrettyTable()
        product_table.field_names = ['Category Name', 'Sales']
        for r in result:
            product_table.add_row([r[0], r[1]])
        print(product_table)
        cursor.close()
        connection.close()
    except BaseException as err:
        print(err)

def ageCategorizationUsers():
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        string_to_execute = "SELECT CASE WHEN strftime('%Y', 'now')-strftime('%Y', U.date_of_birth) < 18 THEN 'Kids(Under 18)' " \
                            "WHEN strftime('%Y', 'now')-strftime('%Y', U.date_of_birth) >= 18 AND strftime('%Y', 'now')-strftime('%Y', U.date_of_birth) < 25 THEN 'Young Adults(18-25)' " \
                            "WHEN strftime('%Y', 'now')-strftime('%Y', U.date_of_birth) >= 25 AND strftime('%Y', 'now')-strftime('%Y', U.date_of_birth) < 30 THEN 'Adults(25-30)' " \
                            "ELSE 'Mature(30+)' " \
                            "END AS AgeCategories, Count(U.user_id) " \
                            "FROM User as U " \
                            "GROUP BY AgeCategories;"
        cursor.execute(string_to_execute)
        result = cursor.fetchall()
        print("")
        product_table = PrettyTable()
        product_table.field_names = ['Age Categories', 'Number of Users in this Category']
        for r in result:
            product_table.add_row([r[0], r[1]])
        print(product_table)
        cursor.close()
        connection.close()
    except BaseException as err:
        print(err)

def popularPaymentMethods():
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        string_to_execute = "select provider, Count(provider) " \
                            "from PaymentDetails " \
                            "group by provider " \
                            "order by 2 desc "
        cursor.execute(string_to_execute)
        result = cursor.fetchall()
        print("")
        product_table = PrettyTable()
        product_table.field_names = ['Payment Method', 'Usages']
        for r in result:
            product_table.add_row([r[0], r[1]])
        print(product_table)
        cursor.close()
        connection.close()
    except BaseException as err:
        print(err)


