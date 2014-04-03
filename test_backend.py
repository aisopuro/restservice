from backend import Backend, BASE_ARGS
from types import DictType
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import logging as log


class TestBackend():
    '''A unittest class for nosetests. Tests backend and database functionality.
    '''
    def setUp(self):
        log.basicConfig(level=log.DEBUG)
        self.backend = Backend()

    def tearDown(self):
        self.backend = None

    def test_init(self):
        pass

    def test_get_root(self):
        try:
            self.backend.get_root()
        except:
            assert False

    def test_connection(self):
        try:
            obj = self.backend.db.products.find_one()
            log.info(obj)
            assert type(obj) is DictType
        except:
            assert False

    def test_parse_args(self):
        args = ImmutableMultiDict()
        # No args should return base dictionary
        assert self.backend.parse_args(args) == BASE_ARGS
        # Incorrect args should return base dict
        args = ImmutableMultiDict([('dfdd', 'frefrf'), (342, 4334)])
        assert self.backend.parse_args(args) == BASE_ARGS

    def test_get_categories(self):
        categories = set([
            'electronics',
            'books',
            'movies',
            'comics',
            'games'
        ])

        assert categories == set(self.backend.get_categories())

    def test_parse_args_limit(self):
        # Correct arg should return dict with arg as key
        args = ImmutableMultiDict([
            ('limit', 20),
            ('limit', 15)
        ])
        val = self.backend.parse_args(args)
        assert 'limit' in val
        # value should be the last passed parameter
        assert val['limit'] == 15

    def test_parse_args_field(self):
        # giving a field argument should return dict with fields as key
        args = ImmutableMultiDict([
            ('field', 'price'),
            ('notfield', 'description')
        ])
        val = self.backend.parse_args(args)
        assert 'fields' in val
        # Should be dict
        assert type(val['fields']) is dict
        assert 'price' not in val['fields']
        assert not val['fields']['description']

    def test_parse_args_field_id(self):
        # giving a field argument should return dict with fields as key
        args = ImmutableMultiDict([
            ('field', '_id'),
            ('notfield', 'description')
        ])
        val = self.backend.parse_args(args)
        assert 'fields' in val
        # Should be dict
        assert type(val['fields']) is dict
        # _id should be false
        assert not val['fields']['_id']
        assert not val['fields']['description']

    def test_parse_args_category(self):
        args = ImmutableMultiDict([
            ('category', 'electronics'),
            ('notcategory', 'Flim flam')
        ])
        val = self.backend.parse_args(args)
        assert 'spec' in val
        assert 'electronics' in val['spec']['category']['$in']
        assert 'flim flam' in val['spec']['category']['$nin']

    def test_parse_args_price(self):
        args = ImmutableMultiDict([
            ('maxprice', 50),
            ('maxprice', 200)
        ])
        val = self.backend.parse_args(args)
        assert 'price' in val['spec']
        assert '$lt' in val['spec']['price']
        assert val['spec']['price']['$lt'] == 200

    def test_parse_args_subcategory(self):
        args = ImmutableMultiDict([
            ('subcategory', 'computers'),
            ('subcategory', 'strips'),
            ('notsubcategory', 'thriller')
        ])
        val = self.backend.parse_args(args)

        assert 'spec' in val
        assert 'computers' in val['spec']['subcategory']['$in']
        assert 'strips' in val['spec']['subcategory']['$in']
        assert 'thriller' in val['spec']['subcategory']['$nin']

    def test_parse_args_sort(self):
        args = ImmutableMultiDict([
            ('sort', 'category'),
            ('sort', 'subcategory'),
            ('dsort', 'price')
        ])
        val = self.backend.parse_args(args)

        assert 'sort' in val
        for field, direction in val['sort']:
            if field in ['category', 'subcategory']:
                assert direction > 0
            elif field == 'price':
                assert direction < 0
            else:
                assert False

    def test_parse_args_amount(self):
        args = ImmutableMultiDict([
            ('minamount', 0),
            ('minamount', 10),
            ('minamount', 5)
        ])
        val = self.backend.parse_args(args)

        assert 'spec' in val
        assert val['spec']['amount']['$gte'] == 5

    def test_search(self):
        args = {
            'limit': 10,
            'spec': {
                'category': {
                    '$in': ['electronics']
                }
            }
        }
        val = self.backend.search(self.backend.db.products, args)
        assert len(val) == 10
        for doc in val:
            #pprint(doc)
            assert doc['category'] == 'electronics'

    def test_get_products(self):
        args = ImmutableMultiDict([
            ('limit', 10),
            ('category', 'electronics'),
            ('category', 'books'),
            ('subcategory', 'romance'),
            ('subcategory', 'tablet'),
            ('maxprice', 500)
        ])
        val = self.backend.get_products(args)
        assert len(val) == 10
        for doc in val:
            assert doc['category'] in [
                'electronics',
                'books'
            ] and doc['subcategory'] in [
                'romance',
                'tablet'
            ] and doc['price'] <= 500
