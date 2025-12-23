from odoo.tests.common import TransactionCase
from odoo import fields, Command
from datetime import timedelta


class TestLastOrderProduct(TransactionCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()

        self.partner = self.env["res.users"].create(
            {
                "name": "Salesman Test User",
                "login": "sales_test_user",
                "email": "sales_test@example.com",
            }
        )

        # Product 1: Will have an Order
        self.product = self.env["product.product"].create(
            {
                "name": "A Ordered Product",
                "type": "consu",
                "list_price": 100.0,
            }
        )

        # Product 2: Will have an Invoice
        self.product_second = self.env["product.product"].create(
            {
                "name": "B Invoiced Product",
                "type": "consu",
                "list_price": 200.0,
            }
        )

        # Create Order for Product 1
        self.order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.partner_id.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1,
                            "price_unit": 100.0,
                        }
                    )
                ],
            }
        )

        # Create Invoice for Product 2
        self.invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner.partner_id.id,
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product_second.id,
                            "quantity": 1,
                            "price_unit": 200.0,
                        }
                    )
                ],
            }
        )

        # Create Bill for Product
        self.bill = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "partner_id": self.partner.partner_id.id,
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "price_unit": 200.0,
                        }
                    )
                ],
            }
        )

        self.past_time = fields.Datetime.now() - timedelta(hours=1)

    def test_last_order_computation_name_search(self):
        """Test that confirming a sale order updates the last_order and display_name has order time"""
        self.order.action_confirm()
        self.assertEqual(self.order.state, "sale")
        self.order.date_order = self.past_time
        ctx = {"customer": self.partner.partner_id.id, "formatted_display_name": True}
        product_with_ctx = self.product.with_context(ctx)
        product_with_ctx._compute_last_order()
        self.assertEqual(
            product_with_ctx.last_order,
            self.order.date_order,
            "Last order date should match the sale order date",
        )
        results = (
            self.env["product.product"]
            .with_context(ctx)
            .name_search(name=self.product.name)
        )
        ago = self.product.with_context(ctx).compute_agotime(self.order.date_order)
        self.assertEqual(ago, "1h", "Time computed should be 1h")
        result_name = results[0][1]
        self.assertIn("--1h--", result_name, "Name should contain the time suffix")

    def test_last_invoice_date_computation_name_search(self):
        """Test that confirming a create date updates the last_invoice_date and product appear on top"""
        self.invoice.action_post()
        self.assertEqual(self.invoice.state, "posted")
        ctx = {"customer": self.partner.partner_id.id, "formatted_display_name": True}
        product_with_ctx = self.product_second.with_context(ctx)
        product_with_ctx._compute_last_invoice_date()
        self.assertEqual(
            product_with_ctx.last_invoice_date,
            self.invoice.create_date,
            "Last invoice date should match the invoice creation date",
        )
        results = self.env["product.product"].with_context(ctx).name_search(name="")
        self.assertEqual(
            results[0][1],
            self.product_second.name,
            "Recently invoiced product should be on top.",
        )

    def test_no_customer_name_search(self):
        """Test that if no customer is selected then should ive default display_name and sorting"""
        self.invoice.action_post()
        self.order.action_confirm()
        ctx = {"customer": None, "formatted_display_name": True}
        results = self.env["product.product"].with_context(ctx).name_search(name="")
        result_ids = [r[0] for r in results]
        index_product_a = result_ids.index(self.product.id)
        index_product_b = result_ids.index(self.product_second.id)
        self.assertLess(
            index_product_a,
            index_product_b,
            "Without customer context, sorting should default.",
        )
        product_a_result_name = next(r[1] for r in results if r[0] == self.product.id)
        self.assertNotIn(
            "--",
            product_a_result_name,
            "Suffix should not be present without customer context",
        )

    def test_last_invoice_time_compute(self):
        """Test to compute last_invoice_time which depends on last_invoice_date"""
        self.invoice.action_post()
        ctx = {"customer": self.partner.partner_id.id, "order_id": self.order.id}
        product_with_ctx = self.product_second.with_context(ctx)
        product_with_ctx.with_context(ctx)._compute_invoice_time()
        self.assertEqual(
            product_with_ctx.last_invoice_time,
            "Just Now",
            "Last invoice time should be 'Just Now' for less then 1 minute older invoices",
        )

    def test_purchase_order_product_sorting(self):
        """Test to confirming recently purchsed product is on top"""
        self.bill.action_post()
        self.assertEqual(self.bill.state, "posted")
        ctx = {"vendor": self.partner.partner_id.id, "formatted_display_name": True}
        product_with_ctx = self.product.with_context(ctx)
        product_with_ctx._compute_last_invoice_date()
        self.assertEqual(
            product_with_ctx.last_invoice_date,
            self.bill.create_date,
            "Last invoice date should match the bill creation date",
        )
        results = self.env["product.product"].with_context(ctx).name_search(name="")
        self.assertEqual(
            results[0][1],
            self.product.name,
            "Billed product should be at the top for Vendor context",
        )
