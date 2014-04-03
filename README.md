RestService
===========

This is an attempt at making REST service and describe it using WSDL as a course assignment.
This project was made using [Flask](http://flask.pocoo.org/), deployed on [Heroku](https://www.heroku.com/‎) and uses a database provided by [MongoHQ](www.mongohq.com/‎).

This is RestService. You can search for products by going to http://aalto-digi-restservice.herokuapp.com/products/ and adding url query parameters.
You can also go to http://aalto-digi-restservice.herokuapp.com/products/available/ to limit the search to available products. 
Go to http://aalto-digi-restservice.herokuapp.com/products/categories/<category> to search for products in <category>, for example http://aalto-digi-restservice.herokuapp.com/products/categories/electronics.
Going to http://aalto-digi-restservice.herokuapp.com/products/categories/ will return a list of categories in the database.
Query parameters can be used in all of these urls except http://aalto-digi-restservice.herokuapp.com/products/categories/.

Parameters
----------
limit - Number. Give an upper limit of search results to return. Can give many, but only last parameter is processed. Negative values are interpreted as 0.
notfield - String. Give the name of a field that should not be included in the results, i.e "price" will return results that do not give their prices.
category and notcategory - String. The category(ies) that should or shouldn't be included in the results.
subcategory and notsubcategory - String. As with categories, only the more specific subcategory or genre.
maxprice - Number. Set the exclusive maximum price. I.e specifying 400 will return only items whose price is at most 399.99.
sort and dsort - String. Give the name of a field by which to sort up (sort) or down (dsort). Can give many.
minamount - Number. Give the inclusive minimum amount of product that should be in stock. I.e giving 0 means no products that are out of stock are returned. Can give many, but only last parameter is processed.
