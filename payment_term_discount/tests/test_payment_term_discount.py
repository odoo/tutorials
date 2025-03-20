from datetime import timedelta
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo import fields


@tagged("post_install", "-at_install")
class PaymentTermDiscount(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.payment_term = cls.env["account.payment.term"].create(
            {
                "name": "my payment term",
                "early_discount": True,
                "discount_percentage": 50,
                "discount_days": 5,
                "early_pay_discount_computation": "included",
            }
        )
        cls.sub_payment_term1 = cls.env["account.payment.term"].create(
            {
                "name": f"child dicount - {cls.payment_term.name}",
                "early_discount": True,
                "parent_id": cls.payment_term.id,
                "discount_percentage": 40,
                "discount_days": 5,
                "early_pay_discount_computation": "included",
            }
        )
        cls.sub_payment_term2 = cls.env["account.payment.term"].create(
            {
                "name": f"child dicount - {cls.payment_term.name}",
                "early_discount": True,
                "parent_id": cls.payment_term.id,
                "discount_percentage": 20,
                "discount_days": 5,
                "early_pay_discount_computation": "included",
            }
        )
        cls.sub_payment_term3 = cls.env["account.payment.term"].create(
            {
                "name": f"child dicount - {cls.payment_term.name}",
                "early_discount": True,
                "parent_id": cls.payment_term.id,
                "discount_percentage": 10,
                "discount_days": 5,
                "early_pay_discount_computation": "included",
            }
        )

        cls.invoices = cls.env["account.move"].create(
            [
                {
                    "move_type": "out_invoice",
                    "partner_id": cls.env.ref("base.res_partner_12").id,
                    "invoice_date": fields.Date.today(),
                    "invoice_payment_term_id": cls.payment_term.id,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {"name": "My product1", "quantity": 1, "price_unit": 1000},
                        )
                    ],
                },
                {
                    "move_type": "out_invoice",
                    "partner_id": cls.env.ref("base.res_partner_12").id,
                    "invoice_date": fields.Date.today(),
                    "invoice_payment_term_id": cls.payment_term.id,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {"name": "My product2", "quantity": 1, "price_unit": 1000},
                        )
                    ],
                },
            ]
        )

    def test_early_payment_discount_for_mutiple_invoice(self):
        for invoice in self.invoices:
            invoice.invoice_date = fields.Date.today() - timedelta(days=3)
            invoice.action_post()
        wizard = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=self.invoices.ids)
            .create({})
        )
        values = wizard._get_total_amounts_to_pay(wizard.batches)
        first_invoice_amount = (
            self.invoices[0].invoice_line_ids.price_unit
            * self.invoices[0].invoice_line_ids.quantity
        )
        second_invoice_amount = (
            self.invoices[1].invoice_line_ids.price_unit
            * self.invoices[1].invoice_line_ids.quantity
        )
        expected_amount = (
            first_invoice_amount
            - (first_invoice_amount * 50 / 100)
            + second_invoice_amount
            - (second_invoice_amount * 50 / 100)
        )

        self.assertEqual(
            values["amount_by_default"],
            expected_amount,
            "50% discount should be applied.",
        )
        for invoice in self.invoices:
            invoice.button_draft()
            invoice.invoice_date = fields.Date.today() - timedelta(days=7)
            invoice.action_post()
        wizard = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=self.invoices.ids)
            .create({})
        )
        values = wizard._get_total_amounts_to_pay(wizard.batches)
        expected_amount = (
            first_invoice_amount
            - (first_invoice_amount * 40 / 100)
            + second_invoice_amount
            - (second_invoice_amount * 40 / 100)
        )
        self.assertEqual(
            values["amount_by_default"],
            expected_amount,
            "40% discount should be applied.",
        )

        for invoice in self.invoices:
            invoice.button_draft()
            invoice.invoice_date = fields.Date.today() - timedelta(days=12)
            invoice.action_post()
        wizard = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=self.invoices.ids)
            .create({})
        )
        values = wizard._get_total_amounts_to_pay(wizard.batches)
        expected_amount = (
            first_invoice_amount
            - (first_invoice_amount * 20 / 100)
            + second_invoice_amount
            - (second_invoice_amount * 20 / 100)
        )
        self.assertEqual(
            values["amount_by_default"],
            expected_amount,
            "20% discount should be applied.",
        )

        for invoice in self.invoices:
            invoice.button_draft()
            invoice.invoice_date = fields.Date.today() - timedelta(days=18)
            invoice.action_post()
        wizard = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=self.invoices.ids)
            .create({})
        )
        values = wizard._get_total_amounts_to_pay(wizard.batches)
        expected_amount = expected_amount = (
            first_invoice_amount
            - (first_invoice_amount * 10 / 100)
            + second_invoice_amount
            - (second_invoice_amount * 10 / 100)
        )
        self.assertEqual(
            values["amount_by_default"],
            expected_amount,
            "10% discount should be applied.",
        )

        for invoice in self.invoices:
            invoice.button_draft()
            invoice.invoice_date = fields.Date.today() - timedelta(days=22)
            invoice.action_post()
        wizard = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=self.invoices.ids)
            .create({})
        )
        values = wizard._get_total_amounts_to_pay(wizard.batches)
        expected_amount = expected_amount = first_invoice_amount + second_invoice_amount
        self.assertEqual(
            values["amount_by_default"],
            expected_amount,
            "No discount should be applied.",
        )
