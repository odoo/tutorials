# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests import Form


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.buyer = cls.env['res.partner'].create({
            'name': 'buyer',
        })
        cls.properties = cls.env['estate.property'].create([{
            'name': 'prop1',
            'expected_price': 10000,
        }])
        cls.offers = cls.env['estate.property.offer'].create([{
            'partner_id': cls.buyer.id,
            'property_id': cls.properties[0].id,
            'price': 9000,
        }])

    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""
        # You cannot sell a property without an accepted offer
        with self.assertRaises(UserError):
            self.properties.action_sold()

        # accept the offer
        self.offers[0].action_accept()
        self.assertEqual(self.properties.buyer_id, self.buyer)
        self.assertEqual(self.properties.selling_price, 9000)   
        # Now you can sell it
        self.properties.action_sold()
        self.assertEqual(self.properties.state, 'sold')
        self.assertRecordValues(self.properties, [
           {'state': 'sold'},
        ])

        # You cannot create an offer for a sold property
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create([{
                'partner_id': self.buyer.id,
                'property_id': self.properties[0].id,
                'price': 10000,
            }])

    def test_property_form(self):
        """Test the form view of properties."""
        with Form(self.properties[0]) as prop:
            self.assertEqual(prop.garden_area, 0)
            self.assertIs(prop.garden_orientation, False)
            prop.garden = True
            self.assertEqual(prop.garden_area, 10)
            self.assertEqual(prop.garden_orientation, "north")
            prop.garden = False
            self.assertEqual(prop.garden_area, 0)
            self.assertIs(prop.garden_orientation, False)
