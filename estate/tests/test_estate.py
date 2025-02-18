# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged

@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        """ Set up test data before running the test cases. """
        super(EstateTestCase, cls).setUpClass()

        cls.buyer = cls.env['res.partner'].create({
            'name': 'buyer',
        })

        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 10000,
        })

        cls.offer = cls.env['estate.property.offer'].create({
            'partner_id': cls.buyer.id,
            'property_id': cls.property.id,
            'price': 9000,
        })

    def test_action_sell(self):
        self.property.state = 'sold_offer'
        with self.assertRaises(UserError, msg="Selling a property without an accepted offer!"):
            self.property.action_sold()

        self.offer.action_accept()

        self.assertEqual(self.property.buyer_id, self.buyer, msg="Buyer not matched!")
        self.assertEqual(self.property.selling_price, 9000, msg="Selling price not matched!")

        self.property.action_sold()
        self.assertEqual(self.property.state, 'sold_offer', msg="State not changes to sold offer!")

        self.assertRecordValues(self.property, [
            {'state': 'sold_offer'},
        ])

        with self.assertRaises(UserError, msg="Can't create an offer, as property already been sold!"):
            self.env['estate.property.offer'].create({
                'partner_id': self.buyer.id,
                'property_id': self.property.id,
                'price': 10000,
            })

    def test_property_form(self):
        with Form(self.property) as prop:
            self.assertEqual(prop.garden_area, 0, msg="check default value of garden_area")
            self.assertIs(prop.garden_orientation, False, msg="check default value of garden_orientation")

            prop.garden = True
            self.assertEqual(prop.garden_area, 10, msg="Garden is set, so default value would'nt work!")
            self.assertEqual(prop.garden_orientation, "north")

            prop.garden = False
            self.assertEqual(prop.garden_area, 0, msg="Garden is reset, default value would work!")
            self.assertIs(prop.garden_orientation, False)
