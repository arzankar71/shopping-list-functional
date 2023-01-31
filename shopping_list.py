from typing import (
    List,
    Dict,
    Tuple
)
import os
import json
import datetime
import random
from enum import Enum
import help


vegetables: Dict[str, float] = {'onion': 3.8, 'turnip': 11.6, 'celery': 13.8}
fruits: Dict[str, float] = {'apple': 5.1, 'orange': 4.2, 'banana': 14.0}
dairy: Dict[str, float] = {'milk': 5.3, 'butter': 15.1, 'cheese': 4.3}


class Menu(Enum):
    Show = 1
    Remove = 2
    Search = 3
    Category = 4
    Filter = 5
    Gift = 6
    Wallet = 7
    Buy = 8
    Logout = 9


EXIT: Tuple[str] = ("quit", "q", "ex", "exit")
shopping_list: List[str] = list()
shopping_price: List[float] = list()
gift: List[str] = list()

# define a function that show the current day


def today() -> str:
    time = datetime.date.today()
    today = time.strftime("%d/%m")
    return today


# define a function for registering users

def user_register(username: str, password: str, birthdate: str, phone: str, wallet: str) -> bool: # noqa E50 
    """
    This is for registering in website.
    user must fill the fields with his/her information
    """
    is_authenticated = False
    # This is a dictionary which contains user's information
    # It'll be added to a list,then this list will be stored in database
    user_information = dict()
    with open('user.json', 'r') as user_file:
        user = json.load(user_file)

    user_information["username"] = username
    user_information["password"] = password
    user_information["birthday"] = birthdate.strftime("%d/%m")

    user_information["phone"] = phone
    user_information["wallet"] = wallet
    phone_user = list(filter(lambda user: user['phone'] == user_information["phone"], user)) # noqa E50 
    if not phone_user:
        user.append(user_information)
        with open('user.json', 'w') as user_file:
            json.dump(user, user_file, indent=4)
            print("you 've registered successfully,please login")
            is_authenticated = True
    else:
        print("This account hes been registered before")
    return is_authenticated


# define a function for entrance of users in website


def user_login(log_name: str, log_password: str) -> bool:
    """
    This is for logging into website.
    User can log into website by entering the correct username and password
    Parameters:
    log_name:user's name field
    log_password:user's password field
    """
    is_authenticated = False
    # This is a list which can be appended when user logs in
    # The values of it:user's birthday and money
    # It 'll be stored in database(json file) later.
    # This ia a sign that shows the user is still in the website
    # It is valuable when user wants to charge the money or use birthday gift
    birth_wallet: List = list()
    login_name: str = log_name
    login_password: str = log_password
    with open('user.json', 'r') as user_file:
        users = json.load(user_file)
    user_filter = list(filter(lambda user: user['username'] == login_name and user['password'] == login_password, users)) # noqa E50 
    if user_filter:
        is_authenticated = True
        person_birth = user_filter[0]['birthday']
        person_wallet = user_filter[0]['wallet']
        person_phone = user_filter[0]['phone']
        birth_wallet.append(person_birth)
        birth_wallet.append(person_wallet)
        birth_wallet.append(person_phone)
        with open('birth_wallet.json', 'w') as birth_wallet_file:
            json.dump(birth_wallet, birth_wallet_file)
            print(f"Hi {user_filter[0]['username']}")
            print("welcome to our shop")

    else:
        print("username or password is wrong")
    return is_authenticated


# define a function to offer discount because of user's birthday

def birthday_gift(product: Dict[str, float], shopping: List[str], price: List[float], gift: List[str]): # noqa E50 
    """
    It decreases the price of one product to 50 percent randomly if was the user's birthday. # noqa E50 
    Parameters:
    product:the dictionary of products.it can be fruits,vegetables or dairy
    shopping:user's shopping_list.It is just the name of products the user wants to buy # noqa E50 
    price:The list of product's price which user wants to buy.
    gift:is a list which can be empty.It shows the items can be offered because of user's birthday. # noqa E50 
    """

    products = product.items()
    # choose one item randomly from specific dictionary(fruits,vegetables or dairy) # noqa E50 
    random_item = random.choice(list(products))
    # decrease the price of item to 50 percent
    new_price = random_item[1]
    new_price -= (new_price * 1/2)
    print(f"because of your birthday,{random_item[0]} is {new_price}")
    question = input("Do you want to add this item to your list? ")
    if question == "yes":
        # Adding the item which website offer discount on to user's shopping list # noqa E50 
        gift.append(random_item[0])
        shopping.append(random_item[0])
        price.append(new_price)
        print(f"{random_item[0]} added to your list successfully")
    """

    Parameters

    'product' :
    the dictionary that specify the type of items
    'shopping' :
    the list we named shopping_list that shows the items that user wants to buy
    'price' :
    the list we named shopping_price that shows the price of items we want to buy # noqa E50 
    'gift' :
    the list we named gift to show the item we want to offer discount for user's birthday # noqa E50 
    """


# defining a function for showing our list in column type


def beautify_list(shopping_name: List[str], shopping_price: List[float]):
    """
    It just integrates two lists(shopping_list,shopping_price) into one list
    It shows the user his/her shopping basket better.
    Parameters
    `shopping_name` :
    the list we named shopping_list that shows the items that user wants to buy

    `shopping_price` :
    the list we named shopping_price that shows the price of items we want to buy # noqa E50   
    """
    name_price_list = list(zip(shopping_name, shopping_price))
    for item in name_price_list:
        print(f"name:{item[0]} price:{item[1]}")

# defining a function to help the user


def show_help():
    """
    It helps the user to know how to have a good shopping.
    It shows the user the menu of website
    """
    print(help.show)
    print(help.remove)
    print(help.search)
    print(help.category)
    print(help.filter)
    print(help.gift)
    print(help.wallet)
    print(help.buy)
    print(help.logout)


# defining a function to add item in shopping list


def add_item(shopping_list: List[str], products: Dict[str, float], price: List[float], item: str): # noqa E50 
    """
    It adds the name and price of products to shopping list and
    shopping price respectively
    Parameters
    shopping_list,products,price,item----------
    item:
    the item we want to add to shopping_list
    shopping_list :
    the list we named shopping_list that shows the items that user wants to buy
    products :
    the dictionaries that show the type of item we want to buy
    price :
    the list we named shopping_price.It shows the price of items we want to buy

    Returns
    -------


    """
    if item in shopping_list:
        print("sorry,The item has already added")
    else:
        shopping_list.append(item)
        price.append(products[item])
        print(f"{item} added to your list successfully")


# defining a function to remove an item from shopping list


def remove_item(products: List[str], price: List[float], item: str) -> List[str]: # noqa E50 
    """
    It removes the items user wants to remove from his/her shopping_list
    Parameters
    products,price,item----------
    my_list :
    shopping_list,shopping_price
    item :
    the item we want ro remove from shopping_list
    products :
    the list we named shopping_list that shows the items that user wants to buy
    price :
    the list we named shopping_price.It shows the price of items we want to buy

    Returns
    the name and price of item user wants to remove from shopping_list-------


    """
    if item not in products:
        print("item that you are trying to remove is not in the list")
    else:
        index_item = products.index(item)
        products.remove(item)
        price.pop(index_item)
    return products, price


def clear_screen():
    """ """
    return os.system('clear')

# a function to show the item we searched


def show_item(product: Dict[str, float], item: str):
    """
    It just shows the name and price of items when user is searching
    Parameters
    product,item----------
    my_list :
    the type of item that user wants to see
    item :
    the item user searched
    product :
    the type of item that user searched

    Returns
    -------


    """

    print(f"name:{item} price:{product[item]}")


# a function to show the items user wants to buy


def show_products(products: Dict[str, float]):
    """
    It just shows the products of one type.
    For example all the items of fruit.It is used when user enter 'category'
    Parameters
    products----------
    products :
    the items which there is in the category that user wants to see

    Returns
    -------

    """
    for product in products:
        print(f"name:{product} price:{products[product]}")

# a function to show filtered products


def show_filtered_items(item: List[Tuple[str, float]]):
    """
    It just shows the items that user filter by price
    Parameters:
    item:This ia list which contains tuples.tuples contain name and price of products the user filter # noqa E50 
    """
    for key, value in item:
        print(f"name:{key} price:{value}")

# a function to sum the price of items want to buy


def invoice(price: List[str]) -> float:
    """
    This is for when user wants to finalize his/her birthday.
    It shows the invoice of user's shopping
    Parameters
    price :
    the list we named shopping_price.It shows the price of items we want to buy

    Returns
    the total of price of items the user wants to buy-------

    """
    total = 0
    for item in price:
        total += item
    return float(total)


user_log_reg = input("Do you want to login or register?").casefold()
clear_screen()
if user_log_reg == "register":
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        birthday = input("Enter your Birthday (in DD/MM): ")
        birthdate = datetime.datetime.strptime(birthday, "%d/%m")
        phone = input("Enter your phone number: ")
        wallet = float(input("How much do you charge your wallet? ")) # noqa E50 
        if user_register(username, password, birthdate, phone, wallet):
            break

    while True:
        name_login = input("Enter your name: ")
        password_login = input("Enter your password:")
        if user_login(name_login, password_login):
            break

elif user_log_reg == "login":
    while True:
        name_login = input("Enter your name: ")
        password_login = input("Enter your password:")
        if user_login(name_login, password_login):
            break

# Infinite loop
while True:

    menu = input(
        "what do you want to do? ").casefold()
    clear_screen()

    # To jump out of loop and show shopping list

    if menu in EXIT:
        with open('birth_wallet.json', 'r') as birth_wallet_file:
            birth_wallet = json.load(birth_wallet_file)
        birth_wallet_clean = birth_wallet.clear()
        with open('birth_wallet.json', 'w') as birth_wallet_file:
            json.dump(birth_wallet_clean, birth_wallet_file)
        break

    # To help the user

    elif menu == "help":
        show_help()

    # To show  shopping list

    elif menu == str(Menu.Show.value):
        beautify_list(shopping_list, shopping_price)

    # To remove an item in shopping list

    elif menu == str(Menu.Remove.value):
        item_remove = input("please enter the item you want to remove: ")
        remove_item(shopping_list, shopping_price, item_remove)

    # To show the item for which user is looking

    elif menu == str(Menu.Search.value):
        search_for_item = input("Enter the item you are looking for: ")
        if search_for_item in vegetables:
            show_item(vegetables, search_for_item)
            question_add_vegetables = input("Do you want to add this item to your list? ") # noqa E50 
            if question_add_vegetables == "yes":
                add_item(shopping_list, vegetables, shopping_price, search_for_item) # noqa E50

        elif search_for_item in fruits:
            show_item(fruits, search_for_item)
            question_add_fruits = input("Do you want to add this item to your list? ") # noqa E50 
            if question_add_fruits == "yes":
                add_item(shopping_list, fruits, shopping_price, search_for_item) # noqa E50 
        elif search_for_item in dairy:
            show_item(dairy, search_for_item)
            question_add_dairy = input("Do you want to add this item to your list? ") # noqa E50 
            if question_add_dairy == "yes":
                add_item(shopping_list, dairy, shopping_price, search_for_item)
        else:
            print(f"Sorry,there is no {search_for_item} in list")

    # if user wants to see an item in it's category

    elif menu == str(Menu.Category.value):
        product_kind = input("what kinds of product you want to see? ")
        if product_kind == "vegetables":
            show_products(vegetables)
            which_vegetable = input("which one do you add to your list? ")
            if which_vegetable in vegetables:
                add_item(shopping_list, vegetables, shopping_price, which_vegetable) # noqa E50

        if product_kind == "fruits":
            show_products(fruits)
            which_fruit = input("which one do you add to your list? ")
            if which_fruit in fruits:
                add_item(shopping_list, fruits, shopping_price, which_fruit)

        if product_kind == "dairy":
            show_products(dairy)
            which_dairy = input("which one do you add to your list? ")
            if which_dairy in dairy:
                add_item(shopping_list, dairy, shopping_price, which_dairy)

    # To filter products for user considering price

    elif menu == str(Menu.Filter.value):
        filter_item = input("you can see products less or more than 10 dollars: ") # noqa E50 
        if filter_item == "less":
            # Find items which their price is less then 10
            less_vegetables = list(filter(lambda item: item[1] < 10, vegetables.items())) # noqa E50 
            less_fruits = list(filter(lambda item: item[1] < 10, fruits.items())) # noqa E50 
            less_dairy = list(filter(lambda item: item[1] < 10, dairy.items()))
            show_filtered_items(less_vegetables)
            show_filtered_items(less_fruits)
            show_filtered_items(less_dairy)
        elif filter_item == "more":
            # Find items which their price is less then 10
            more_vegetables = list(filter(lambda item: item[1] >= 10, vegetables.items())) # noqa E50 
            more_fruits = list(filter(lambda item: item[1] >= 10, fruits.items())) # noqa E50 
            more_dairy = list(filter(lambda item: item[1] >= 10, dairy.items())) # noqa E50 
            show_filtered_items(more_vegetables)
            show_filtered_items(more_fruits)
            show_filtered_items(more_dairy)

    # User's birthday gift
    elif menu == str(Menu.Gift.value):
        if not gift:
            with open('birth_wallet.json', 'r') as birth_file:
                birthday = json.load(birth_file)
            # birthday is a list that has 2 values,value[0] is user's birthday
            # Value[1] is user's wallet
            if birthday[0] == today():
                print("Happy Birthday")
                day = datetime.date.today()
                today_num = int(day.strftime("%w")) + 1
                # If the day was Sunday or Monday,the gift would be from vegetables # noqa E50 
                if 1 <= today_num < 3:
                    birthday_gift(vegetables, shopping_list, shopping_price, gift) # noqa E50 
                # If the day was Tuesday or Wednesday,the gift would be from fruits # noqa E50 
                if 3 <= today_num < 5:
                    birthday_gift(fruits, shopping_list, shopping_price, gift)
                # If the day was Thursday,Friday or Saturday,the gift would be from dairy # noqa E50 
                if 5 <= today_num < 8:
                    birthday_gift(dairy, shopping_list, shopping_price, gift)
            else:
                print("You don't have a gift")
        else:
            print("sorry,you've used your gift before")

    # To charge the money
    elif menu == str(Menu.Wallet.value):
        with open('birth_wallet.json', 'r') as birth_wallet_file:
            birth_wallet = json.load(birth_wallet_file)

        print(f"Your account balance is {birth_wallet[1]}")
        wallet = float(input("How much do you want to charge? "))
        birth_wallet[1] += wallet

        with open('birth_wallet.json', 'w') as birth_wallet_file:
            json.dump(birth_wallet, birth_wallet_file)

    # To finalize the shopping

    elif menu == str(Menu.Buy.value):
        if shopping_list:
            with open('birth_wallet.json', 'r') as birth_wallet_file:
                birth_wallet = json.load(birth_wallet_file)

            if invoice(shopping_price) <= birth_wallet[1]:
                birth_wallet[1] -= invoice(shopping_price)
                with open('birth_wallet.json', 'w') as birth_wallet_file:
                    json.dump(birth_wallet, birth_wallet_file)
                beautify_list(shopping_list, shopping_price)
                print(f"Your final invoice is {invoice(shopping_price)}")
                shopping_list.clear()
                shopping_price.clear()
            else:
                print("your account balance is not enough")
                print("please charge your wallet")

    # To log out the website
    elif menu == str(Menu.Logout.value):
        with open('birth_wallet.json', 'r') as birth_wallet_file:
            birth_wallet = json.load(birth_wallet_file)
        birth_wallet_clean = birth_wallet.clear()
        with open('birth_wallet.json', 'w') as birth_wallet_file:
            json.dump(birth_wallet_clean, birth_wallet_file)
        break
