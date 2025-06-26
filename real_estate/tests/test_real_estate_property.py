from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged

@tagged('post_install', '-at_install')
class RealEstateTestCase(TransactionCase):
    def setUp(self):
        super(RealEstateTestCase, self).setUp()

        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })

        self.property = self.env['real.estate.property'].create({
            'name': 'Property 1',
            'expected_price': 10000,
            'garden': True,
            'garden_area': 100.0,
            'garden_orientation': 'north',
        })

        self.offer = self.env['real.estate.property.offer'].create({
            'price': 12000,
            'property_id': self.property.id,
            'validity': 10,
            'partner_id': self.partner.id
        })
    
    def test_create_offer_for_sold_property(self):
        self.property.write({'status': 'sold'})

        with self.assertRaises(UserError):
            self.env['real.estate.property.offer'].create({
                'price': 13000,
                'property_id': self.property.id,
                'validity': 12,
                'partner_id': self.partner.id
            })
    
    def test_sell_property_no_offer_accepted(self):
        with self.assertRaises(UserError):
            self.property.action_property_sold()

    def test_sell_property_with_accepted_offer(self):
        self.offer.write({'status': 'accepted'})
        self.property.action_property_sold()
        self.assertEqual(self.property.status, 'sold', "The property should be marked as sold.")

    def test_garden_uncheck (self):
        form = Form(self.property)
        form.garden = False

        self.assertEqual(form.garden_area, 0, "The garden area should be reset to 0")
        self.assertEqual(form.garden_orientation, False, "The garden orientation should be reset")
    
    def test_garden_check(self):
        form = Form(self.property)
        form.garden = False
        form.garden = True

        self.assertEqual(form.garden_area, 10, "The garden area should be 0")
        self.assertEqual(form.garden_orientation, 'north', "The garden orientation should be empty")
