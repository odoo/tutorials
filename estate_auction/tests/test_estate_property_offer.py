# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestEstatePropertyOffer(TransactionCase):

    def setUp(self):
        super(TestEstatePropertyOffer, self).setUp()
        self.partner = self.env['res.partner'].create({'name': 'Test Partner'})
        self.property = self.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 100000,
            'sale_type': 'auction'
        })

    def test_create_offer_valid(self):
        """Test creating a valid offer above the expected price."""
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 110000,
            'partner_id': self.env.ref('base.res_partner_1').id
        })
        self.assertTrue(offer, "Offer creation failed")

    def test_create_offer_below_expected_price(self):
        """Test that offers with price below best price are rejected."""
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'price': 90000,
                'partner_id': self.env.ref('base.res_partner_1').id
            })

    def test_update_offer_price_valid(self):
        """Test updating an offer price to a higher valid amount."""
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 110000,
            'partner_id': self.env.ref('base.res_partner_1').id
        })
        offer.write({'price': 120000})
        self.assertEqual(offer.price, 120000, "Offer price update failed")

    def test_update_offer_price_below_expected_price(self):
        """Test that updating an offer price below expected price is rejected."""
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 110000,
            'partner_id': self.env.ref('base.res_partner_1').id
        })
        with self.assertRaises(UserError):
            offer.write({'price': 90000})
