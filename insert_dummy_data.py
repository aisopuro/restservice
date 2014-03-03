from backend import Backend
from random import randint, randrange

back = Backend()

products = back.db.products

base_doc = {
    'name': '',
    'description': '',
    'category': '',
    'subcategory': '',
    'price': 0.0
}


def insert(name, description, category, subcategory, minprice, maxprice, pricestep=1, amount=100):
    print (subcategory),
    for i in range(0, amount):
        doc = base_doc.copy()
        doc['name'] = name % i
        doc['description'] = description
        doc['category'] = category
        doc['subcategory'] = subcategory
        doc['price'] = randrange(minprice, maxprice, pricestep) + 0.99
        doc['amount'] = randint(0, 50)
        products.insert(doc)
        if i % 10 == 0:
            print ('.'),
    print 'done'

insert('Computer nr %i', 'Lots of processors', 'electronics', 'computers', 249, 2999, 10, 100)
insert('Tablet nr %i', 'Shiny', 'electronics', 'tablet', 249, 799, 20, 50)
insert('Phone nr %i', 'Handy', 'electronics', 'mobile', 149, 699, 20, 20)
insert('Thriller nr %i', 'Erudite', 'books', 'thriller', 9, 24, 100)
insert('Romance nr %i', 'Lovely', 'books', 'romance', 4, 19, 100)
insert('Movie nr %i', 'Gripping', 'movies', 'suspense', 9, 19, 5, 50)
insert('Romance Movie nr %i', 'Gripping', 'movies', 'romance', 9, 19, 5, 50)
insert('Comic nr %i', 'Graphic', 'comics', 'strips', 14, 29, 3, 70)
insert('Accessory nr %i', 'Accessible', 'electronics', 'accessories', 39, 149, 5, 100)
insert('Game nr %i', 'Interactive', 'games', 'action-adventure', 4, 59, 5, 100)
insert('Horror Game nr %i', 'Interactive', 'games', 'horror', 4, 59, 5, 100)
