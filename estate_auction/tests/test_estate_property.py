# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({'name': 'Test Partner'})
        self.property = self.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 100000,
            'sale_type': 'auction',
            'auction_end_time': datetime.now() + timedelta(hours=24)
        })

    def test_compute_highest_offer(self):
        """Test computation of the highest offer."""
        offer1 = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 110000,
            'partner_id': self.env.ref('base.res_partner_1').id
        })
        offer2 = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 120000,
            'partner_id': self.env.ref('base.res_partner_1').id
        })
        self.property._compute_highest_offer()
        self.assertEqual(self.property.highest_offer, 120000, "Highest offer computation failed")

    def test_compute_highest_bidder(self):
        """Test computing the highest bidder based on offers."""
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 130000,
            'partner_id': self.partner.id
        })
        self.property._compute_highest_bidder()
        self.assertEqual(self.property.highest_bidder_id, self.partner, "Highest bidder computation failed")

    def test_action_start_auction(self):
        """Test starting an auction successfully."""
        self.property.action_start_auction()
        self.assertTrue(self.property.auction_started, "Auction should be started")
        self.assertEqual(self.property.auction_status, 'auction', "Auction status should be updated")

    def test_action_start_auction_already_started(self):
        """Test that starting an already started auction raises an error."""
        self.property.auction_started = True
        with self.assertRaises(UserError):
            self.property.action_start_auction()

    def test_action_generate_invoice(self):
        """Test generating an invoice for a sold property."""
        self.property.status = 'sold'
        self.property.selling_price = 150000
        self.property.buyer_id = self.partner
        result = self.property.action_generate_invoice()
        self.assertTrue(self.property.invoice_id, "Invoice should be created")

    def test_action_generate_invoice_not_sold(self):
        """Test that generating an invoice for an unsold property is rejected."""
        with self.assertRaises(UserError):
            self.property.action_generate_invoice()
