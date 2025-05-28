from odoo.tests import tagged
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestProductWarranty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
                "list_price": 100.0,
                "has_warranty": True,
            }
        )
        cls.warranty_product = cls.env["product.product"].create(
            {
                "name": "Standard Warranty",
                "type": "service",
            }
        )
        cls.warranty = cls.env["product.warranty"].create(
            {
                "name": "Standard Warranty",
                "product_id": cls.warranty_product.id,
                "percentage": 10.0,
                "year": 1,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )
        cls.sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
            }
        )

    def test_product_warranty_creation(self):
        """Test creation of a product warranty."""
        warranty = self.env["product.warranty"].create(
            {
                "name": "Extended Warranty",
                "product_id": self.warranty_product.id,
                "percentage": 15.0,
                "year": 2,
            }
        )
        self.assertEqual(warranty.name, "Extended Warranty")
        self.assertEqual(warranty.percentage, 15.0)
        self.assertEqual(warranty.year, 2)

    def test_product_warranty_unique_name(self):
        """Test uniqueness constraint on warranty name."""
        with self.assertRaises(ValidationError):
            self.env["product.warranty"].create(
                {
                    "name": "Standard Warranty",
                    "product_id": self.warranty_product.id,
                    "percentage": 10.0,
                    "year": 1,
                }
            )

    def test_sale_order_line_warranty_fields(self):
        """Test warranty-related fields in sale order line."""
        order_line = self.env["sale.order.line"].create(
            {
                "order_id": self.sale_order.id,
                "product_id": self.product.id,
                "product_uom_qty": 1,
                "price_unit": 100.0,
                "warranty": True,
                "warranty_product_id": self.warranty.id,
                "is_warranty": False,
            }
        )
        self.assertTrue(order_line.warranty)
        self.assertEqual(order_line.warranty_product_id, self.warranty)

    def test_product_template_has_warranty_field(self):
        """Test has_warranty field in product template."""
        self.assertTrue(self.product.has_warranty)

        self.product.has_warranty = False
        self.assertFalse(self.product.has_warranty)

    def test_add_warranty(self):
        """Test adding warranty through the wizard."""
        order_line = self.env["sale.order.line"].create(
            {
                "order_id": self.sale_order.id,
                "product_id": self.product.id,
                "product_uom_qty": 1,
                "price_unit": 100.0,
                "warranty": False,
                "is_warranty": False,
            }
        )

        wizard_line = self.env["product.warranty.wizard.line"].create(
            {
                "order_line_id": order_line.id,
                "product_id": self.product.id,
                "warranty_product_id": self.warranty.id,
            }
        )

        wizard = (
            self.env["product.warranty.wizard"]
            .with_context(active_id=self.sale_order.id)
            .create(
                {
                    "wizard_line_ids": [(6, 0, [wizard_line.id])],
                }
            )
        )

        wizard.add_warranty()
        warranty_line = order_line.warranty_orderline
        self.assertTrue(warranty_line, "Warranty line was not created.")
        self.assertEqual(
            warranty_line.order_id,
            self.sale_order,
            "Warranty line is not linked to the correct sale order.",
        )
