from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstatePropertyOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.sold_property = cls.env['estate.property'].create(
            {
                'name': "sold property",
                'expected_price': 100,
                'state': 'sold'
            }
        )

        cls.partner = cls.env['res.partner'].create(
            {
                'type': 'contact',
                'name': "partner"
            }
        )

    def test_create_offer_on_property(self):
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create(
                {
                    'price': self.sold_property.expected_price,
                    'property_id': self.sold_property.id,
                    'partner_id': self.partner.id
                }
            )
