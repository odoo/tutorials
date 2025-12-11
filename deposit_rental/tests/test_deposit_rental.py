from odoo.fields import Command
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestDepositRental(TransactionCase):

    def setUp(self):
        super().setUp()

        self.deposit_product = self.env["product.product"].create({
            "name": "Rental Deposit",
            "type": "service",
            "list_price": 50.0
        })

        self.rental_product = self.env["product.product"].create({
            "name": "Projectore Rental",
            "type": "consu",
            "require_deposit": True,
            "list_price": 100.0
        })

        self.env["ir.config_parameter"].sudo().set_param("sale_renting.deposit_product_id", self.deposit_product.id)
        self.partner = self.env["res.partner"].create({"name": "Test Customer"})

    def test_rental_product_deposit_amount(self):
        """Test that the rental product correctly requires a deposit."""
        self.assertEqual(self.rental_product.deposit_amount, self.deposit_product.list_price, "Deposit amount mismatch!")

    def test_sale_order_deposit_creation(self):
        sale_order = self.env["sale.order"].create({"partner_id": self.partner.id})
        sale_order.write({
            "order_line": [
                Command.create({"product_id": self.rental_product.id, "product_uom_qty": 2}),
            ]
        })
        deposit_line = sale_order.order_line.filtered(lambda l: l.is_deposit_line)
        linked_product = deposit_line.linked_line_id.product_id

        self.assertEqual(linked_product.id, self.rental_product.id, "Deposit line is not linked to the expected product!")
        self.assertEqual(deposit_line.product_id, self.deposit_product, "Incorrect deposit product!")
        self.assertEqual(deposit_line.price_unit, self.deposit_product.list_price, "Deposit amount not calculated correctly!")
        self.assertEqual(deposit_line.product_uom_qty, deposit_line.linked_line_id.product_uom_qty, "Deposit quantity does not match rental product quantity!")

    def test_sale_order_copy(self):
        """Test that a duplicated order does not copy deposit lines but creates new ones."""
        sale_order = self.env["sale.order"].create({"partner_id": self.partner.id})

        sale_order.write({
            "order_line": [
                Command.create({"product_id": self.rental_product.id, "product_uom_qty": 1}),
            ]
        })

        copied_order = sale_order.copy()

        self.assertNotEqual(copied_order.order_line, sale_order.order_line, "Lines should not be directly copied!")
        self.assertEqual(len(copied_order.order_line.filtered(lambda line: line.is_deposit_line)), 1, "Deposit should be recreated!")
