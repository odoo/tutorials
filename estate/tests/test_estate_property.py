# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.property = self.env['estate.property'].create({
            'name': 'Test Property 1',
            'expected_price': 100,
        })

    def test_total_area(self):
        self.property.living_area = 20
        self.property.garden_area = 30
        self.assertRecordValues(self.property, [
           {'total_area': 50},
        ])

    def test_cannot_create_offer_for_sold_property(self):
        self.property.state = 'sold'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'price': 100,
                'property_id': self.property.id
            })

    def test_cannot_sell_property_without_accepted_offer(self):
        with self.assertRaises(UserError):
            self.property.action_sold()

    def test_can_sell_property_with_accepted_offer(self):
        offer = self.env['estate.property.offer'].create({
            'price': 100,
            'property_id': self.property.id,
            'partner_id': 1,
            'state': 'accepted'
        })
        self.property.action_sold()
        self.assertEqual(self.property.state, 'sold')

    def test_cannot_cancel_after_sold(self):
        self.property.state = 'sold'
        with self.assertRaises(UserError):
            self.property.action_cancel()
