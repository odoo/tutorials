# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class EstatePropertyOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.sold_property = cls.env['estate.property'].create(
            {'name': 'Sold Property', 'expected_price': 100000, 'state': 'sold'}
        )
        cls.partner = cls.env['res.partner'].create({'type': 'contact', 'name': 'Partner 1'})

    def test_create_offer_on_sold_property(self):
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create(
                {
                    'property_id': self.sold_property.id,
                    'price': self.sold_property.expected_price,
                    'partner_id': self.partner.id,
                }
            )
