from helpers import add_product_path
from storageOps import *
from Product import ProductInOrder

print()
print("Welcome to User Login System")
print()
running = True
while running:
    print()
    primary_choice = int(input("""Choose an option:
    1. Create New User or Login
    2. Exit
    """))
    if primary_choice == 1:
        choice = input("New User Y or N ?: ").upper()
        if choice == "Y":
            print()
            print("To create an account, please fill in the information below.")
            print()
            email = input("Email: ")
            password = input("Password: ")
            firstname = input("First Name: ")
            lastname = input("Last Name: ")
            address = input("Address: ")
            telephone = input("Telephone: ")
            date_of_birth = input("Date of Birth: ")
            create_user(email, password, firstname, lastname, address, telephone, date_of_birth)
            print()
            print("User account created successfully!")
        if choice == "N":

            print()
            print("To access your account, please enter your credentials below.")
            print()
            email = input("Email: ")
            password = input("Password: ")
            valid_login = validate_login_details(email, password)
            if valid_login != False:
                print()
                print("Logged in successfully!")
                second_running = True
                while second_running:
                    secondary_choice = int(input("""Choose an option:
                        1. View Categories
                        2. View your cart
                        3. View your orders
                        4. Checkout
                        5. Exit
                        """))
                    if secondary_choice == 1:
                        add_product_path(valid_login)
                    if secondary_choice == 2:
                        view_cart(valid_login)
                    if secondary_choice == 3:
                        view_orders(valid_login)
                    if secondary_choice == 4:
                        provider = int(input("""Choose a provider:
                        1. Amex
                        2. Mastercard
                        3. Visa
                        4. BHIM
                        """))
                        checkout_cart_items(valid_login, provider)
                    if secondary_choice == 5:
                        second_running = False
            else:
                print("\n")
                print("Account does not exist")
                continue
    if primary_choice == 2:
        print()
        print("Goodbye!")
        running = False
