import server
from unittest import TestCase
from json import loads
from pprint import pprint


class TestServer(TestCase):
    '''A unittest class for nosetests. Tests server urls.
    '''

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def tearDown(self):
        self.app = None

############TESTING##########################

    def test_root(self):
        assert '200' in self.app.get('/').status
        assert '405' in self.app.post('/').status

    def test_products_limit(self):
        response = self.app.get('/products/?limit=10')
        assert '200' in response.status
        r_list = loads(response.data)
        assert type(r_list) is list
        assert len(r_list) == 10

    def test_products_sort(self):
        response = self.app.get('/products/?sort=amount&limit=30')
        assert '200' in response.status
        r_list = loads(response.data)
        assert len(r_list) == 30
        prev = 0
        for item in r_list:
            assert item['amount'] >= prev
            prev = item['amount']

    def test_products_available(self):
        response = self.app.get('/products/available?limit=10')
        assert '200' in response.status
        r_list = loads(response.data)
        assert len(r_list) == 10
        for item in r_list:
            assert item['amount'] > 0

    def test_products_category(self):
        response = self.app.get('/products/categories/electronics?limit=10')
        assert '200' in response.status
        r_list = loads(response.data)
        assert len(r_list) == 10
        for item in r_list:
            assert item['category'].lower() == 'electronics'
