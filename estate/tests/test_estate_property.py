from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import tagged, TransactionCase


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({'name': 'Test Partner'})
        self.property = self.env['estate.property'].create({
            'name': 'Test Property',
            'description':'check'
        })
        self.offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 100000,
            'partner_id': self.partner.id
        })

    def test_cannot_create_offer_for_sold_property(self):
        self.property.state = 'sold'
        with self.assertRaises(ValidationError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'price': 120000,
                'partner_id': self.partner.id
            })

    def test_cannot_sell_property_without_accepted_offer(self):
        with self.assertRaises(UserError):
            self.property.action_sell_property()

    def test_can_sell_property_with_accepted_offer(self):
        self.property.state = 'offer_accepted'
        self.property.action_sell_property()
        self.assertEqual(self.property.state, 'sold')
