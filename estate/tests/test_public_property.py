from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests import Form, TransactionCase

@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = cls.env['public.property'].create({
            'name': 'Test Property',
            'state': 'new',
            'living_area': 20,
            'expected_price': 1000,
            'garden': True,
            'garden_area': 20,
            'garden_orientation': 'north',
        })  
    def test_offer_creation_on_sold_property(self):
        self.property.state = 'sold'

        with self.assertRaises(UserError):
            self.env['public.property.offer'].create({
                'price': 100000,
                'property_id': self.property.id,
                'partner_id': self.env.ref('base.res_partner_12').id,
            })
        print('===========Test Complete============')

    def test_sell_without_accepted_offer(self):
        self.env['public.property.offer'].create({
            'price': 95000,
            'property_id': self.property.id,
            'partner_id': self.env.ref('base.res_partner_12').id,
        })

        with self.assertRaises(UserError):
            self.property.action_sold()
        print('===========Test Complete============')

    def test_successful_property_sale(self):
        offer = self.env['public.property.offer'].create({
            'price': 95000,
            'property_id': self.property.id,
            'partner_id': self.env.ref('base.res_partner_12').id,
        })

        offer.action_confirm()
        self.property.action_sold()
        self.assertEqual(self.property.state, 'sold')
        print('===========Test Complete============')

    def test_garden_reset_on_uncheck(self):
        property_form = Form(self.property)
        property_form.garden = False
        property_form.save()

        self.assertEqual(self.property.garden_area, 0)
        self.assertFalse(self.property.garden_orientation)
        print('===========Test Complete============')