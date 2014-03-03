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


def insert(name, description, category, subcategory, minprice, maxprice, pricestep=1, amount=50):
    print (subcategory),
    for i in range(0, amount):
        doc = base_doc.copy()
        doc['name'] = name % i
        doc['description'] = description
        doc['category'] = category
        doc['subcategory'] = subcategory
        doc['price'] = randrange(minprice, maxprice, pricestep) + 0.99
        doc['amount'] = randint(0, 100)
        products.insert(doc)
        if i % 10 == 0:
            print ('.'),
        print 'done'

insert('Computer nr %i', 'Lots of processors', 'Electronics', 'Computers', 249, 2999, 10, 100)
insert('Tablet nr %i', 'Shiny', 'Electronics', 'Tablet', 249, 799, 20, 50)
insert('Phone nr %i', 'Handy', 'Electronics', 'Mobile', 149, 699, 20, 20)
insert('Thriller nr %i', 'Erudite', 'Books', 'Thriller', 9, 24, 100)
insert('Romance nr %i', 'Lovely', 'Books', 'Romance', 4, 19, 100)
insert('Movie nr %i', 'Gripping', 'Movies', 'Suspense', 9, 19, 5, 50)
insert('Comic nr %i', 'Graphic', 'Graphic novels', 'Comic strips', 14, 29, 3, 70)
insert('Accessory nr %i', 'Accessible', 'Electronics', 'Accessories', 39, 149, 5, 100)
insert('Game nr %i', 'Interactive', 'Games', 'Action Adventure', 4, 59, 5, 100)
