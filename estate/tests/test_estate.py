# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.tests import Form, tagged
from odoo.exceptions import UserError
from odoo import Command

@tagged('post_install', '-at_install')
class TestEstate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner'
        })

        cls.properties = cls.env['estate.property'].create([
            {
            'name': 'Test Property 1',
            'expected_price': 10000,
            },
            {
                'name': 'Test Property 2',
                'expected_price': 20000,
                'offer_ids': [
                    Command.create({
                        'price': 30000,
                        'partner_id': cls.partner.id,
                        'status': 'accepted'
                    })
                ],
                'state': 'offer_accepted'
            }
        ])

    def test_action_sold(self):
        self.properties[1].action_sold()
        self.assertEqual(self.properties[1].state, 'sold')

        with self.assertRaises(UserError):
            self.properties[0].action_sold()

    def test_create_offer(self):
        self.properties[1].action_sold()

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.properties[1].id,
                'price': 5000000,
                'partner_id': self.partner.id
            })

    def test_garden_reset(self):
        with Form(self.properties[0]) as property:
            property.garden = True
            property.garden_area = 45
            property.garden_orientation = 'south'

            property.garden = False
            property.garden = True
            
            self.assertEqual(property.garden_area, 10)
            self.assertEqual(property.garden_orientation, 'north')
