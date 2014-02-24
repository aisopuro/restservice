from backend import Backend
from types import DictType
from werkzeug.datastructures import ImmutableMultiDict
import logging as log


class TestBackend():
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
        log.info('test_connection')
        try:
            obj = self.backend.db.products.find_one()
            log.info(obj)
            assert type(obj) is DictType
        except:
            assert False

    def test_parse_args(self):
        args = ImmutableMultiDict()
        # No args should return empty dictionary
        assert self.backend.parse_args(args) == {}
        # Incorrect args should return empty dict
        args = ImmutableMultiDict([('dfdd', 'frefrf'), (342, 4334)])
        assert self.backend.parse_args(args) == {}

    def test_parse_args_limit(self):
        # Correct arg should return dict with arg as key
        args = ImmutableMultiDict([
            ('limit', 20),
            ('limit', 15)
        ])
        val = self.backend.parse_args(args)
        assert 'limit' in val
        # value should be the first passed parameter
        assert val['limit'] == 20

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

    def test_parse_args_category(self):
        args = args = ImmutableMultiDict([
            ('category', 'Electronics'),
            ('notcategory', 'Flim flam')
        ])
        val = self.backend.parse_args(args)
        assert 'spec' in val
        assert val['spec']['Electronics']['$exists']
        assert not val['spec']['Flim flam']['$exists']
