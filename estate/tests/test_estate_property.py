from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env['estate.property'].create([{
            'name': 'property 1',
            'expected_price': 100,
        }])

        cls.partner = cls.env['res.partner'].create([{
            'name': 'myCompany',
        }])

    def test_sell_no_offer(self):
        Offer = self.env['estate.property.offer'].create([{
            'price': 92,
            'property_id': self.properties.id,
            'partner_id': self.partner.id,
        }])

        self.properties.offer_ids = [Offer.id]

        with self.assertRaises(UserError):
            self.properties.action_sold()

        self.assertRecordValues(self.properties, [
           {'state': 'Offer Received'},
        ])

    def test_offer_sold_property(self):
        Offer = self.env['estate.property.offer'].create([{
            'price': 93,
            'property_id': self.properties.id,
            'partner_id': self.partner.id,
        }])

        self.properties.offer_ids = [Offer.id]
        Offer.action_accept()
        self.properties.action_sold()

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create([{
                'price': 94,
                'property_id': self.properties.id,
                'partner_id': self.partner.id,
            }])

        self.assertEqual(len(self.properties.offer_ids), 1)
