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
            },
        ])

    def test_offer_on_sold_property(self):
        self.env['estate.property.offer'].create({
            'property_id': self.properties[0].id,
            'price': 110000,
            'partner_id': self.env['res.partner'].create({'name': 'Test Partner1'}).id,
            'status': 'accepted',
        })
        self.properties[0].action_set_sold()
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.properties[0].id,
                'price': 120000,
                'partner_id': self.env['res.partner'].create({'name': 'Test Partner2'}).id,
            })
