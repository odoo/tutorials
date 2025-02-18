# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, AccessError
from odoo.tests import Form, tagged


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.property = self.env['estate.property'].create({
            'name': 'Test Property 1',
            'expected_price': 100,
        })
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner 1',
        })

    def test_total_area(self):
        self.property.living_area = 20
        self.property.garden_area = 30
        self.assertRecordValues(self.property, [
           {'total_area': 50},
        ])

    def test_cannot_create_offer_for_sold_property(self):
        self.property.state ='sold'
        # self.property.write({ 'state': 'sold' })
        # self.property.action_sold()
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'price': 100,
                'property_id': self.property.id,
            })

    def test_cannot_sell_property_without_accepted_offer(self):
        with self.assertRaises(UserError):
            self.property.action_sold()

    def test_can_sell_property_with_accepted_offer(self):
        offer = self.env['estate.property.offer'].create({
            'price': 100,
            'state': 'accepted',
            'property_id': self.property.id,
            'partner_id': self.partner.id,
        })
        self.property.state = 'offer_accepted'
        self.property.action_sold()
        self.assertEqual(self.property.state, 'sold')

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
