from storageOps import *


def add_product_path(valid_login):
    choice = "Y"
    while choice == "Y":
        result = view_categories(None)
        if result == False:
            print("invalid category id entered")
        else:
            tertiary_choice = int(input("""Choose the id of category you want to select: """))
            result = view_categories(tertiary_choice)
            while result != True:
                if result == False:
                    print("invalid category id entered")
                    break
                tertiary_choice = int(input("""Choose the id of category you want to select: """))
                result = view_categories(tertiary_choice)
            print("Enter product id and quantity of the product you want to add to cart:- ")
            product_id = int(input("Product id:- "))
            quantity = int(input("Quantity:- "))
            add_to_cart(valid_login, [ProductInOrder(product_id, quantity, None, None)])
            choice = input("Would you like to continue:- Y or N ?").upper()


