from odoo.tests import TransactionCase
from odoo.exceptions import UserError


class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        cls.properties = cls.env['estate.property'].create([
            {'name': 'House 1', 'state': 'offer_accepted', 'expected_price': '1000'},
            {'name': 'House 2', 'state': 'new', 'expected_price': '1000'},
            {'name': 'House 3', 'state': 'sold', 'expected_price': '1000'},
        ])

    def test_action_sell(self):
        with self.assertRaises(UserError):
            self.properties.action_sell_property()

        self.assertRecordValues(self.properties, [
            {'name': 'House 1', 'state': 'offer_accepted'},
            {'name': 'House 2', 'state': 'new'},
            {'name': 'House 3', 'state': 'sold'},
        ])

        self.properties[1].state = 'offer_accepted'
        self.properties.action_sell_property()

        self.assertRecordValues(self.properties, [
            {'name': 'House 1', 'state': 'sold'},
            {'name': 'House 2', 'state': 'sold'},
            {'name': 'House 3', 'state': 'sold'},
        ])
