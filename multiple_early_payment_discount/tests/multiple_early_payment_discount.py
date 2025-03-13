from datetime import timedelta

from odoo import fields
from odoo.tests import TransactionCase


class TestEarlyPaymentDiscount(TransactionCase):

    def setUp(self):
        super().setUp()

        self.payment_term = self.env["account.payment.term"].create({
            "name": "Test Payment Term"
        })
        self.discount = self.env["account.payment.term.discount"].create({
            "payment_term_id": self.payment_term.id,
            "discount_percentage": 5.0,
            "discount_days": 10
        })
        self.partner = self.env["res.partner"].create({"name": "Test Partner"})
        self.invoice = self.env["account.move"].create({
            "partner_id": self.partner.id,
            "move_type": "out_invoice",
            "invoice_date": fields.Date.today(),
            "invoice_payment_term_id": self.payment_term.id
        })
        self.invoice_line = self.env["account.move.line"].create({
            "move_id": self.invoice.id,
            "name": "Test Product",
            "debit": 100.0
        })
        self.payment_register = self.env["account.payment.register"].create({
            "amount": 100.0,
            "payment_date": fields.Date.today()
        })

    def test_apply_discount_early_payment(self):
        self.payment_register._apply_early_payment_discount(self.payment_register)

        expected_discount = 100.0 * (5.0 / 100.0)
        expected_amount = 100.0 - expected_discount

        self.assertAlmostEqual(self.payment_register.payment_difference, expected_discount, places=2)
        self.assertAlmostEqual(self.payment_register.amount, expected_amount, places=2)

    def test_no_discount_after_expiry(self):
        self.payment_register.payment_date = fields.Date.today() + timedelta(days=15)
        self.payment_register._apply_early_payment_discount(self.payment_register)

        self.assertEqual(self.payment_register.payment_difference, 0.0)
        self.assertEqual(self.payment_register.amount, 100.0)

    def test_no_discount_if_no_payment_term(self):
        self.invoice.invoice_payment_term_id = False
        self.payment_register._apply_early_payment_discount(self.payment_register)

        self.assertEqual(self.payment_register.payment_difference, 0.0)
        self.assertEqual(self.payment_register.amount, 100.0)

    def test_unique_constraint_on_discount_days(self):
        with self.assertRaises(Exception):
            self.env["account.payment.term.discount"].create({
                "payment_term_id": self.payment_term.id,
                "discount_percentage": 3.0,
                "discount_days": 10
            })
