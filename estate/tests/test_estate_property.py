# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged

@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()

        self.partner = self.env['res.partner'].create({
            'name': 'salesperson',
        })

        self.property1 = self.env['estate.property'].create({            
            'name':'test1',
            'expected_price':100.00,
            'buyer_id': self.partner.id,
        })

        self.offer1 = self.env['estate.property.offer'].create({
            'price':100.00,
            'property_id':self.property1.id,
            'partner_id':self.property1.buyer_id.id
        })

        self.offer2 = self.env['estate.property.offer'].create({
            'price':100.00,
            'property_id':self.property1.id,
            'partner_id':self.property1.buyer_id.id
        })

    def test_create_no_offer_if_sold(self):
        self.property1.state='sold'
        with self.assertRaises(UserError):
            self.property1.offer_ids.create({
                'price':100.00,
                'property_id':self.property1.id,
                'partner_id':self.property1.buyer_id.id
            })

    def test_no_sold_before_offer_accepted(self):
        self.env['estate.property.offer'].create({
            'price':100.00,
            'property_id':self.property1.id,
            'partner_id':self.property1.buyer_id.id
            })
        with self.assertRaises(UserError):
            self.property1.set_property_sold()
    
    def test_sold(self):
        self.offer1.accept_offer()
        self.assertEqual(self.property1.selling_price,100.00)
        self.property1.set_property_sold()
        self.assertEqual(self.property1.state,'sold')

        with self.assertRaises(UserError):
            self.offer2.accept_offer()

    def test_property_form(self):
        with Form(self.property1) as prop:
            self.assertEqual(prop.garden_area, 0, msg="check default value of garden_area")
            self.assertIs(prop.garden_orientation, False, msg="check default value of garden_orientation")

            prop.garden = True
            self.assertEqual(prop.garden_area, 10, msg="Garden is set, so default value would'nt work!")
            self.assertEqual(prop.garden_orientation, "north")

            prop.garden = False
            self.assertEqual(prop.garden_area, 0, msg="Garden is reset, default value would work!")
            self.assertIs(prop.garden_orientation, False)
