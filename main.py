__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import *
from populate_test_database import populate_test_database


def close_enough_search(term, text):
    """
    Returns Whether a given term matches with any of the words in a given text.

    matching rules:
        Depending on length of term string {>=10, >=6, >=3} either 3, 2 or 1 characters can be different between given word and term.
        If all other character (case-insensitive) are the same between word and term for the same indices then it counts as a match.
        If the substring word[0:len(term)] is a perfect match (no different characters) then the word is a match.
        If a word is longer than the search term it is NOT a match.

        term ("play") will match with "playing"
        term ("ploy") will match with "play"
        term ("cumfertibly") will match with "comfortably"

    Args:
        term (string): Term being looked for
        text (string): Text being looked through

    Returns:
        (bool): True or False whether the text contains exactly or close enough to the specified term.
    """
    term = term.lower()
    text = text.lower()
    words = text.split(" ")

    NUMBER_OF_MISSES_ALLOWED = 0
    if len(term) >= 10:
        NUMBER_OF_MISSES_ALLOWED = 3
    elif len(term) >= 6:
        NUMBER_OF_MISSES_ALLOWED = 2
    elif len(term) >= 3:
        NUMBER_OF_MISSES_ALLOWED = 1

    for word in words:
        if len(term) > len(word):
            continue
        misses = 0
        for i in range(len(term)):
            if term[i] != word[i]:
                misses += 1
        if misses == 0:
            return True
        if misses <= NUMBER_OF_MISSES_ALLOWED and len(term) == len(word):
            return True
    return False


def search(term):
    all_products = Product.select()
    products = []
    for product in all_products:
        if close_enough_search(term, product.name) or close_enough_search(term, product.description):
            products.append(product)
    return products

def list_user_products(user_id):
    return list(Product.select().join(User).where(User.id == user_id))


def list_products_per_tag(tag_id):
    return list(Product.select().join(ProductTag).where(ProductTag.tag_id == tag_id))


def add_product_to_catalog(user_id, product):
    user = User.get_or_none(User.id == user_id)
    tags = product.pop("tags", None)
    if not user:
        return
    product = Product.create(owned_by=user, **product)
    if tags:
        product.tags.add(tags)
    

def update_stock(product_id, new_quantity):
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        return
    product.quantity = new_quantity
    product.save()


def purchase_product(product_id, buyer_id, quantity):
    product = Product.get_or_none(Product.id == product_id)
    buyer = User.get_or_none(User.id == buyer_id)
    if not product or not buyer or quantity > product.quantity:
        print("Not enough items in stock!")
        return
    
    Transaction.create(buyer = buyer, product = product, quantity = quantity)
    product.quantity -= quantity

    product.save()


def remove_product(product_id):
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        return
    product.delete_instance()

    # Remove entries for deleted Item from through model
    ProductTag.delete().where(ProductTag.product_id == product_id).execute()
