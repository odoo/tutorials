# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo import Command


@tagged("post_install", "-at_install")
class TestAddingWarranty(TransactionCase):

    def setUp(self):
        super().setUp()

        self.partner = self.env["res.partner"].create({"name": "Test Partner"})

        self.product_with_warranty = self.env["product.product"].create(
            {
                "name": "Product with Warranty",
                "is_warranty_available": True,
                "type": "consu",
                "list_price": 100.0,
            }
        )

        self.extended_warranty_product = self.env["product.product"].create(
            {
                "name": "Extended Warranty",
                "type": "service",
            }
        )

        self.warranty_config_1year = self.env["warranty.configuration"].create(
            {
                "name": "1 Year Warranty",
                "product_id": self.extended_warranty_product.id,
                "percentage": 10.0,
                "period": 1,
            }
        )

        self.sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_with_warranty.id,
                            "product_uom_qty": 1,
                            "price_unit": self.product_with_warranty.list_price,
                        }
                    )
                ],
            }
        )

    def test_add_warranty_to_sale_order(self):
        """Test if warranty is correctly added to a sale order"""

        sale_order_line_p1 = self.sale_order.order_line.filtered(
            lambda l: l.product_id == self.product_with_warranty
        )

        self.assertTrue(sale_order_line_p1, "Sale order line should exist.")

        warranty_wizard = self.env["sale.order.add.warranty"].create(
            {
                "sale_order_id": self.sale_order.id,
                "warranty_line_ids": [
                    Command.create(
                        {
                            "sale_order_line_id": sale_order_line_p1.id,
                            "warranty_id": self.warranty_config_1year.id,
                        }
                    )
                ],
            }
        )

        warranty_wizard.action_add_warranty()

        warranty_line = self.sale_order.order_line.filtered(
            lambda l: l.product_id == self.warranty_config_1year.product_id
        )

        self.assertTrue(warranty_line, "Warranty should be added to the Sale Order")

        expected_warranty_price = self.product_with_warranty.list_price * (
            self.warranty_config_1year.percentage / 100
        )
        self.assertAlmostEqual(
            warranty_line.price_unit,
            expected_warranty_price,
            places=2,
            msg="Warranty price should be correctly calculated.",
        )

    def test_warranty_button_visibility(self):

        if hasattr(self.sale_order, "show_warranty_button"):
            self.assertTrue(
                self.sale_order.show_warranty_button,
                "Warranty button should be visible when applicable.",
            )

            self.sale_order.order_line.filtered(
                lambda l: l.product_id == self.product_with_warranty
            ).unlink()

            self.assertFalse(
                self.sale_order.show_warranty_button,
                "Warranty button should be hidden when no warranty products exist.",
            )
