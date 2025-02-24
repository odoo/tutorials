# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import ValidationError, UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        """Set up of test data"""
        super(EstateTestCase, cls).setUpClass()

        # Create estate properties
        cls.estate_property_1 = cls.env['estate.property'].create({
            'name' : 'Big Apartment',
            'expected_price' : 15000000,
            'state' : 'offer_accepted'
        })
        cls.estate_property_2 = cls.env['estate.property'].create({
            'name' : 'Luxury Villa',
            'expected_price' : 25000000,
            'state' : 'offer_accepted'
        })

        cls.partner_1 = cls.env.ref('base.res_partner_12')
        cls.partner_2 = cls.env.ref('base.res_partner_2')

        # Create estate property offers
        cls.estate_property_offer_1 = cls.env['estate.property.offer'].create({
            'property_id' : cls.estate_property_1.id,
            'price' : 5500000,
            'partner_id' : cls.partner_1.id,
            'status' : 'accepted'
        })
        cls.estate_property_offer_2 = cls.env['estate.property.offer'].create({
            'property_id' : cls.estate_property_2.id,
            'price' : 7500000,
            'partner_id' : cls.partner_2.id,
            'status' : 'accepted'
        })

    def test_cannot_create_offer_for_sold_property(self):
        """Offer cannot be created for a sold property."""
        self.estate_property_1.state = 'sold'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id' : self.estate_property_1.id,
                'price' : 7500000,
                'partner_id': self.partner_1.id,
                'status' : 'accepted'
            })

    def test_cannot_sell_property_without_accepted_offer(self):
        """Property cannot be sold if no offer is accepted."""
        with self.assertRaises(UserError):
            self.estate_property_1.action_sold()

    def test_property_is_marked_as_sold_correctly(self):
        """Selling a property with an accepted offer updates the state."""
        self.estate_property_offer_1.status = 'accepted'
        self.estate_property_1.state = 'offer_accepted'
        self.estate_property_1.action_sold()
        self.assertEqual(self.estate_property_1.state, 'sold', "The property should be marked as sold.")
