from hashlib import sha3_512
import random
import datetime
import math

from models import *

TAG_NAMES = ["Clothes", "Food", "Tech", "Sports", "Home and Living", "Art"]



USERS = [
    {
        "name": "Lori Runolfsdottir",
        "address": "498 Alberto Terrace, Tatyanaston, Hawkes Bay, 7450",
        "products": [
            {
                "name": "Tennis Racket",
                "description": "Used for playing tennis.",
                "price_per_unit_cents": 30000,
                "quantity": 2,
                "tag_indices": [3] 
            },
            {
                "name": "Couch",
                "description": "Seen better days but still sits comfortably.",
                "price_per_unit_cents": 100000,
                "quantity": 1,
                "tag_indices": [4]
            },
            {
                "name": "Juggling Balls",
                "description": "Who doesn't want to join the circus.",
                "price_per_unit_cents": 3,
                "quantity": 5,
                "tag_indices": [3, 4]
            }
        ]
    },
    {
        "name": "Otha Swaniawski",
        "address": "05 Tess Parade, Generalston, Wellington, 3412",
        "products": [
            {
                "name": "Car",
                "description": "Gets you from A to B.",
                "price_per_unit_cents": 100000,
                "quantity": 1,
                "tag_indices": [4],
            }
        ]
    },
    {
        "name": "Eleazar Wilderman",
        "address": "19 Stroman Place, Erwinston, Southland, 7972",
        "products": [
            {
                "name": "Pots",
                "description": "Cooks up a good meal",
                "price_per_unit_cents": 1000,
                "quantity": 3,
                "tag_indices": [1,4],
            },
            {
                "name": "Coffee Beans (200g)",
                "description": "Tasty Brazillain Coffee",
                "price_per_unit_cents": 9500,
                "quantity": 4,
                "tag_indices": [1, 4],
            }
        ]
    },
    {
        "name": "Ora Weissnat",
        "address": "9 Faustino Quay, Tabithaston, Bay of Plenty, 7757",
        "products": []
    },
    {
        "name": "Elliott Mayer",
        "address": "70 Medhurst Close, Staceyston, Waikato, 0325",
        "products": []
    },
    {
        "name": "Rubie Koss",
        "address": "820 Bins Crescent, Dianaston, Tasman, 1960",
        "products": [
            {
                "name": "Coloured Pencils",
                "description": "Every color you can imagine",
                "price_per_unit_cents": 320,
                "quantity": 10,
                "tag_indices": [5],
            },
            {
                "name": "Mugs",
                "description": "For your morning coffee",
                "price_per_unit_cents": 525,
                "quantity": 4,
                "tag_indices": [4],
            },
            {
                "name": "TV",
                "description": "Flat screen plasma tv.",
                "price_per_unit_cents": 30000,
                "quantity": 1,
                "tag_indices": [2],
            }
        ]
    },
    {
        "name": "Rupert Pagac",
        "address": "29 Homenick Square, Savanahville, Tasman, 0863",
        "products": [
            {
                "name": "Tinned Beans",
                "description": "Delicious in any meal.",
                "price_per_unit_cents": 200,
                "quantity": 8,
                "tag_indices": [2],
            },
            {
                "name": "Books",
                "description": "For your reading pleasure",
                "price_per_unit_cents": 1250,
                "quantity": 7,
                "tag_indices": [4]
            },
        ]
    },
    {
        "name": "Raquel Ebert",
        "address": "89 Kuhlman Line, Dustinston, Wellington, 3106",
        "products": [
            {
                "name": "T Shirts",
                "description": "Fashionable t-shirts. What are you waiting for?",
                "price_per_unit_cents": 530,
                "quantity": 12,
                "tag_indices": [0],
            },
            {
                "name": "Plants (Monstera)",
                "description": "Brighten up your house with some green.",
                "price_per_unit_cents": 1000,
                "quantity": 4,
                "tag_indices": [4],
            },
        ]
    },
    {
        "name": "Mitchell Howell",
        "address": "7 Kuvalis Avenue, Tyrellston, Auckland, 4100",
        "products": [
            {
                "name": "E-Bike",
                "description": "Still runs okay but the gears no longer work. Needs some T.L.C.",
                "price_per_unit_cents": 5000,
                "quantity": 1,
                "tag_indices": [2, 3],
            },
        ]
    },
    {
        "name": "Hilma Douglas",
        "address": "28 Angus Grove, Darianston, Southland, 9644",
        "products": [
            {
                "name": "Football boots",
                "description": "Boots to play football in.",
                "price_per_unit_cents": 2500,
                "quantity": 1,
                "tag_indices": [0,3],
            },
            {
                "name": "DVDS",
                "description": "Nice films to watch on a lazy sunday.",
                "price_per_unit_cents": 550,
                "quantity": 20,
                "tag_indices": [4],
            },
            {
                "name": "IPhone",
                "description": "IPhone 5 still works perfectly.",
                "price_per_unit_cents": 15000,
                "quantity": 1,
                "tag_indices": [2],
            },
        ]
    },
]

def encrypt(data):
    # Used to simulate storing sensitive information with an encryption
    # Not secure for real world application
    return sha3_512(data.encode("utf-8")).hexdigest()

def generate_random_credit_card_number():
    DIGITS = "1234567890"
    result = ""
    for _ in range(16):
        result += random.choice(DIGITS)
    return result

def get_random_expiry_date():
    date_today = datetime.date.today()
    month = date_today.month
    year = date_today.year
    months_till_expiry = random.randint(1, 60)
    month += months_till_expiry
    month -= 1 # Zero index months for modular arithmatic
    year += math.floor(month / 12)
    month %= 12
    month += 1 # Return to 1 index
    return datetime.date(month = month, year = year, day = 1)
    

def get_random_cvv():
    DIGITS = "1234567890"
    result = ""
    for _ in range(3):
        result += random.choice(DIGITS)
    return result

def populate_test_database():
    # clear the tables
    User.delete().execute()
    Product.delete().execute()
    Transaction.delete().execute()
    Tag.delete().execute()
    ProductTag.delete().execute()
    
    TAGS = []
    for name in TAG_NAMES:
        tag = Tag.create(name=name)
        TAGS.append(tag)

    for user in USERS:
        products = []
        if "products" in user:
            products = user.pop("products")

        user["credit_card_number"] = encrypt(generate_random_credit_card_number())
        user["credit_card_expiry"] = get_random_expiry_date()
        user["credit_card_cvv"] = encrypt(get_random_cvv())
        person = User.create(**user)

        for product in products:
            tags = []
            tag_indices = product.pop("tag_indices")
            for i in tag_indices:
                tags.append(TAGS[i])
            p = Product.create(owned_by=person, **product)
            p.tags.add(tags)
