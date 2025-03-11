# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from datetime import timedelta


class TestReferralGiftCards(TransactionCase):

    def setUp(self):
        super().setUp()
        
        self.partner_referrer = self.env['res.partner'].create({'name': 'Referrer Partner'})
        self.partner_customer = self.env['res.partner'].create({
            'name': 'Customer Partner',
            'referred_by': self.partner_referrer.id
        })

        self.pos_order = self.env['pos.order'].create({
            'partner_id': self.partner_customer.id,
            'amount_total': 1000,
            'state': 'paid'
        })

    def test_no_referral_no_gift_card(self):
        print("Test 1")
        """Test that no gift card is created if customer has no referrer"""
        partner = self.env['res.partner'].create({'name': 'No Referral Partner'})
        order = self.env['pos.order'].create({'partner_id': partner.id, 'amount_total': 500, 'state': 'paid'})

        order.create_referral_gift_card()
        gift_card = self.env['loyalty.card'].search([('partner_id', '=', partner.id)])
        
        self.assertFalse(gift_card, "No gift card should be created if customer has no referrer.")
        print("Test 1 passed")
