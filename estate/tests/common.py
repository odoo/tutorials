from odoo.tests import TransactionCase


class TestEstateCommon(TransactionCase):
    def setUp(cls):

        super().setUp()

        cls.property = cls.env['estate.property'].create(
            {'name': 'Test property 1', 'description': 'Test description 1', "expected_price": 1000},
        )
