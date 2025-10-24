from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged('post_install', '-at_install')
class EstatePropertySoldTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):

        super().setUpClass()

        cls.property = cls.env['estate.property'].create(
            [{
                'name': 'Beautiful House',
                'expected_price': 100000,
            }]
        )
    
    def test_sell_offer(self):
        
        # (1) Try to sell a property with no offer.
        with self.assertRaises(UserError):
            self.property.sell_property()

        partner = self.env['res.partner'].create(
            [{
                'name': 'My Favorite Partner'
            }]
        )
        offer = self.env['estate.property.offer'].create(
            [{
                'price': 95000,
                'partner_id': partner.id,
                'property_id': self.property.id
            }]
        )

        # (2) After creating an offer, try to sell the property with no accepted offer.
        with self.assertRaises(UserError):
            self.property.sell_property()

        offer.status = 'accepted'
        self.property.sell_property()

        # (3) After selling it, verify the state of the property.
        self.assertEqual(self.property.state, 'sold')

        # (4) Lastly, verify that we cannot create an offer for a sold property.
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'partner_id': partner.id,
                'property_id': self.property.id,
            })

    def test_garden_checkbox(self):

        property_form = Form(self.property)
        property_form.garden = True

        # (1) Verify the default values of the garden area and orientation.
        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, "north")

        property_form.garden_area = 120
        property_form.garden_orientation = "south"

        # (2) Reset the garden to False and check the default values.
        property_form.garden = False
        self.assertEqual(property_form.garden_area, 0)
        self.assertIsNot(property_form.garden_orientation, True)

        # (3) Reset the garden to True and verify the default values of the garden area and orientation.
        property_form.garden = True
        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, "north")
