from odoo.tests.common import TransactionCase
from odoo.tests import Form
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestEstatePropertyLogic(TransactionCase):

    def setUp(self):
        super().setUp()
        Property = self.env['estate.property']
        Offer = self.env['estate.property.offer']
        self.partner = self.env['res.partner'].create({
            'name': 'Test Buyer',
            'email': 'buyer@example.com'
        })
        self.property = Property.create({
            'name': 'Test Property',
            'state': 'new',
            'expected_price': 150000,
            'garden': True,
            'garden_area': 100,
            'garden_orientation': 'north',
        })
        self.offer = Offer.create({
            'property_id': self.property.id,
            'partner_id': self.partner.id,
            'price': 160000,
        })

    def test_cannot_create_offer_on_sold_property(self):
        self.property.state = 'sold'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': self.partner.id,
                'price': 170000
            })

    def test_cannot_sell_property_without_accepted_offer(self):
        self.property.offer_ids.unlink()
        with self.assertRaises(UserError):
            self.property.action_sold()

    def test_can_sell_property_with_accepted_offer(self):
        self.offer.action_accept()
        self.property.action_sold()
        self.assertEqual(self.property.selling_price, self.offer.price)
        self.assertEqual(self.property.buyer, self.partner)

    def test_reset_garden_fields_when_unchecked(self):
        form = Form(self.env['estate.property'])
        form.name = 'Garden Test'
        form.garden = True
        form.expected_price = 15000
        form.garden_area = 50
        form.garden_orientation = 'east'
        prop = form.save()
        prop.garden = False
        prop._onchange_garden()
        self.assertEqual(prop.garden_area, 0)
        self.assertFalse(prop.garden_orientation)
