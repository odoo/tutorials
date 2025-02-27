from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import tagged, TransactionCase
from odoo.tests import Form


@tagged('post_install', '-at_install', 'estate_test')
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

    def test_onchange_garden_in_form(self):
        with Form(self.property) as form:
            form.garden = True
            self.assertEqual(form.garden_area, 10, "Garden Area should be set as 10")
            self.assertEqual(form.garden_orientation, 'north', "Garden Orientation should be set as North")
            form.garden = False
            self.assertEqual(form.garden_area, 0, "Garden Area should be set to 0 once set Garden is unset")
            self.assertEqual(form.garden_orientation, False, "Garden Orientation should be set to False when Garden unset")
