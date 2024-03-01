from odoo.tests.common import TransactionCase, Form
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class EstateTestProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property = cls.env['estate.property'].create(
            {
                "name": "Logan's House",
                "expected_price": 100000,
            }
        )

        cls.property_sold = cls.env['estate.property'].create(
            {
                "name": "Logan's House 2",
                "expected_price": 120000,
            }
        )

        cls.offer_1 = cls.env['estate.property.offer'].create([
            {
                "price": 100000,
                "partner_id": cls.env.user.partner_id.id,
                "property_id": cls.property_sold.id
            }
        ])

        cls.property_sold.action_set_sold()

    def test_sell_property_with_no_offer(self):
        with self.assertRaises(UserError):
            self.property.action_set_sold()

    def test_add_offer_on_sold_property(self):
        with self.assertRaises(UserError):
            self.offer_2 = self.env['estate.property.offer'].create([
                {
                    "price": 120000,
                    "partner_id": self.env.user.partner_id.id,
                    "property_id": self.property_sold.id
                }
            ])
    
    def test_reset_on_garden_change(self): 
        with Form(self.property) as prop:
            # Initial values
            self.assertRecordValues(self.property, [{
                'garden_area': 0, 'garden_orientation': False
            }])
            # garden must change garden_area and garden_orientation
            prop.garden = True
            prop.save()
            self.assertRecordValues(self.property, [{
                'garden_area': 10, 'garden_orientation': 'north'
            }])
            prop.garden = False
            prop.save()
            self.assertRecordValues(self.property, [{
                'garden_area': 0, 'garden_orientation': False
            }])
