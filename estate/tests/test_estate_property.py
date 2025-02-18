# -- coding: utf-8 --
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

        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 100,
            'state':'offer_accepted'
        })

        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner',
        })

    def test_cannot_create_offer_for_sold_property(self):
        self.property.state = 'sold'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'price': 120,
                'partner_id': self.partner.id,
                'property_id': self.property.id,
            })

    def test_sell_property_without_accepted_offer(self):
        with self.assertRaises(UserError, msg="A property cannot be sold without an accepted offer"):
            self.property.action_sold()

    def test_create_lower_offer_than_existing(self):
        self.env['estate.property.offer'].create({
            'price': 150,
            'partner_id': self.partner.id,
            'property_id': self.property.id,
        })

        with self.assertRaises(UserError , msg="The new offer must be higher than the maximum offer of 150.00"):
             self.env['estate.property.offer'].create({
            'price': 140,
            'partner_id': self.partner.id,
            'property_id': self.property.id,
        })

    def test_cannot_cancel_after_sold(self):
        self.property.state = 'sold'
        with self.assertRaises(UserError):  
            self.property.action_cancel()

    
    def test_property_form(self):
        with Form(self.property) as p:
            self.assertEqual(p.garden_area, 0)
            self.assertIs(p.garden_orientation, False)
            p.garden = True
            self.assertEqual(p.garden_area, 10)
            self.assertEqual(p.garden_orientation, "north")
            p.garden = False
            self.assertEqual(p.garden_area, 0)
            self.assertIs(p.garden_orientation, False)
