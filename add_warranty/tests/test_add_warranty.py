from odoo import Command
from odoo.tests.common import tagged, TransactionCase


@tagged('post_install', '-at_install', 'add_warranty_test')
class TestAddWarranty(TransactionCase):
    def setUp(self):
        super().setUp()
        self.warranty_product = self.env["product.template"].create({
            "name": "Extended Warranty",
            "type": "service",
        })
        self.product_1 = self.env["product.template"].create({
            "name": "Laptop",
            "type": "consu",
            "is_warranty_available": True
        })
        self.product_2 = self.env["product.template"].create({
            "name": "Mobile Phone",
            "type": "consu",
            "is_warranty_available": False
        })
        self.warranty_config = self.env["warranty.configuration"].create({
            "name": "1-Year Warranty",
            "period": 1,
            "product_id": self.warranty_product.id,
            "percent": 10,
        })
        self.sale_order = self.env["sale.order"].create({
            "partner_id": self.env.ref("base.res_partner_1").id,
        })
        self.sale_order_line_1 = self.env["sale.order.line"].create({
            "order_id": self.sale_order.id,
            "product_id": self.product_1.product_variant_id.id,
            "name": "Laptop",
            "price_unit": 1000,
        })
        self.sale_order_line_2 = self.env["sale.order.line"].create({
            "order_id": self.sale_order.id,
            "product_id": self.product_2.product_variant_id.id,
            "name": "Mobile Phone",
            "price_unit": 800,
        })

    def test_warranty_wizard_default_get(self):
        wizard = self.env["sale.order.warranty"].with_context(active_id=self.sale_order.id).create({})
        self.assertIn(self.sale_order_line_1.id, wizard.order_line_ids.ids,"Product with warranty must be present in wizard orderline")
        self.assertNotIn(self.sale_order_line_2.id, wizard.order_line_ids.ids, "Product without warranty must not be present in wizard orderline")

    def test_add_warranty_to_products(self):
        wizard = self.env["sale.order.warranty"].with_context(active_id=self.sale_order.id).create({})
        wizard.order_line_ids[0].warranty_item = self.warranty_config
        wizard.add_warranty_to_products()
        warranty_line = self.sale_order.order_line.filtered(
            lambda line: line.product_id == self.warranty_product.product_variant_id
            and line.related_line_id == self.sale_order_line_1
        )
        self.assertTrue(warranty_line, "Warranty line should be created")
        self.assertEqual(warranty_line.price_unit, 100, "Warranty price should be 10 percent of the original price")
        self.assertEqual(warranty_line.related_line_id, self.sale_order_line_1, "Warranty line must be linked to the correct product")
        self.assertIsNotNone(warranty_line.end_date, "Warranty should have an expiry date")
    
    def test_product_deletes_warranty_line(self):
        wizard = self.env["sale.order.warranty"].with_context(active_id=self.sale_order.id).create({
            "order_line_ids": [Command.set([self.sale_order_line_1.id])],
        })
        wizard.order_line_ids[0].warranty_item = self.warranty_config
        wizard.add_warranty_to_products()
        self.sale_order_line_1.unlink()
        warranty_line = self.sale_order.order_line.filtered(
            lambda line: line.product_id == self.warranty_product.product_variant_id
            and line.related_line_id == self.sale_order_line_1
        )
        self.assertFalse(warranty_line.id, "Corresponding warranty line should be deleted automatically.")
