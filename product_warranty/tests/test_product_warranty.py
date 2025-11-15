from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestProductWarranty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].search(
            [("name", "=", "Deco Addict")], limit=1
        )
        cls.sale_order = cls.env["sale.order"].create({"partner_id": cls.partner.id})
        cls.warranty_products = cls.env["product.product"].search(
            [("is_warranty_available", "=", True)], limit=2
        )
        cls.without_warranty_products = cls.env["product.product"].search(
            [("is_warranty_available", "=", False)], limit=2
        )
        cls.sale_order_lines = cls.env["sale.order.line"].create(
            [
                {"order_id": cls.sale_order.id, "product_id": product.id}
                for product in cls.warranty_products + cls.without_warranty_products
            ]
        )
        cls.wizard = (
            cls.env["product.warranty.wizard"]
            .with_context(
                {"active_model": "sale.order", "active_id": cls.sale_order.id}
            )
            .create({})
        )

    def test_only_warranty_products_in_wizard(self):
        products = self.wizard.wizard_line_ids.mapped("product_id")

        self.assertTrue(
            all(product.is_warranty_available for product in products),
            "Products that don't have warranty boolean ticked are in the wizard",
        )

    def test_warranty_order_line_creation(self):
        warranty = self.env["warranty.config"].search([], limit=1)
        self.wizard.wizard_line_ids[0].warranty_product_id = warranty.id
        product_sequence = self.wizard.wizard_line_ids[0].order_line_id.sequence
        self.wizard.add_warranty()

        self.assertRecordValues(
            self.env["sale.order.line"].search(
                [
                    (
                        "order_id",
                        "=",
                        self.wizard.wizard_line_ids[0].order_line_id.order_id.id,
                    ),
                    ("sequence", "=", product_sequence + 1),
                ]
            ),
            [{"product_id": warranty.product_id.id, "is_warranty_product": True}],
        )
