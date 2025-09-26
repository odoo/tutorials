from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstatePropertyOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstatePropertyOfferTestCase, cls).setUpClass()

        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'Test Property 1',
                'expected_price': 100000,
                'state': 'sold',
            },
        ])

    def test_offer_on_sold_property(self):
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.properties[0].id,
                'price': 100000,
                'partner_id': self.env['res.partner'].create({'name': 'Test Partner'}).id,
            })
