# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import fields
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestLoyaltyCardReferral(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pos_config = cls.env["pos.config"].create({
            "name": "Test POS Config",
            "company_id": cls.env.company.id,
        })
        cls.pos_session = cls.env["pos.session"].create({
            "config_id": cls.pos_config.id,
            "state": "opened"
        })
        cls.referral_program = cls.env["loyalty.program"].create({
            "name": "Gift Cards",
            "program_type": "gift_card",
            "applies_on": "future",
            "trigger": "auto",
            "portal_visible": True,
            "portal_point_name": "$",
            "active": True,
        })
        cls.partner_referrer = cls.env["res.partner"].create({
            "name": "Referrer Partner",
            "referrer": False
        })
        cls.partner_customer = cls.env["res.partner"].create({
            "name": "Customer Partner",
            "referred_by": cls.partner_referrer.id
        })
        cls.pos_order = cls.env["pos.order"].create({
            "partner_id": cls.partner_customer.id,
            "amount_total": 1000,
            "amount_paid": 1000,
            "session_id": cls.pos_session.id,
            "state": "paid",
            "amount_tax": 100,
            "amount_return": 0,
        })

    def test_create_referral_gift_card(self):
        result = self.env["loyalty.card"].create_referral_gift_card(self.partner_customer.id, self.pos_order.amount_total)
        gift_card = self.env["loyalty.card"].search([("partner_id", "=", self.partner_referrer.id)], limit=1)
        self.assertTrue(result, "Gift card creation should return a valid result.")
        self.assertTrue(gift_card, "Gift card should be created for the referrer.")
        self.assertEqual(gift_card.points, 100, "Gift card amount should be 10% of order total.")
        self.assertEqual(gift_card.expiration_date, fields.Date.today() + timedelta(days=90), "Gift card should expire in 90 days.")

    def test_no_gift_card_without_referrer(self):
        partner = self.env["res.partner"].create({"name": "New Customer"})
        order = self.env["pos.order"].create({
            "partner_id": partner.id,
            "amount_total": 500,
            "amount_paid": 500,
            "session_id": self.pos_session.id,
            "state": "paid",
            "amount_tax": 50,
            "amount_return": 0,
        })
        result = self.env["loyalty.card"].create_referral_gift_card(partner.id, order.amount_total)
        gift_card = self.env["loyalty.card"].search([("partner_id", "=", partner.id)])
        self.assertFalse(result)
        self.assertFalse(gift_card)

    def test_cannot_change_referred_by_for_existing_referrer(self):
        self.partner_referrer.write({"referrer": True})
        with self.assertRaises(ValidationError):
            self.partner_referrer.write({"referred_by": self.partner_customer.id})

    def test_no_gift_card_when_loyalty_program_is_inactive(self):
        self.referral_program.write({"active": False})
        result = self.env["loyalty.card"].create_referral_gift_card(self.partner_customer.id, self.pos_order.amount_total)
        gift_card = self.env["loyalty.card"].search([("partner_id", "=", self.partner_referrer.id)])
        self.assertFalse(result, "Gift card creation should return False when the referral program is inactive.")
        self.assertFalse(gift_card, "No gift card should be created when the referral program is inactive.")

    def test_changing_company_type_removes_referral(self):
        self.partner_customer.company_type = "company"
        self.partner_customer._onchange_company_type()
        self.assertFalse(self.partner_customer.referred_by, "Referred_by should be removed when company type is changed to 'company'.")
