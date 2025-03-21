from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged, Form


@tagged("post_install", "-at_install")
class SaleOrderInheritTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(SaleOrderInheritTestCase, cls).setUpClass()
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "barcode": "12345",
                "list_price": 100.0,
                "type": "consu",
            }
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )

        cls.sale_order = cls.env["sale.order"].create(
            {"partner_id": cls.partner.id, "state": "draft", "name": "RANDOM"}
        )

        cls.sale_order_cancelled = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "state": "cancel",
            }
        )

        cls.sale_order_confirmed = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "state": "sale",
            }
        )

    def test_sale_order_state_cancelled(self):
        """Test that a UserError is raised if trying to scan a barcode on a canceled sale order"""
        with self.assertRaises(UserError):
            self.sale_order_cancelled.on_barcode_scanned("12345")

    def test_sale_order_create_line(self):
        """Test that a new line is created when a product is scanned in a draft sale order"""

        with Form(self.sale_order) as form:
            # scan the barcode (simulating user input)
            form._barcode_scanned = "12345"

            # trigger the barcode scan logic (on_barcode_scanned)
            form.save()

        # check that the order now has one line
        self.assertEqual(
            len(self.sale_order.order_line),
            1,
            "Sale order should have 1 line after barcode scan.",
        )

        # ensure the product in the line matches the expected product
        self.assertEqual(
            self.sale_order.order_line.product_id,
            self.product,
            "Product ID in the order line does not match.",
        )

        # ensure the quantity is correctly set to 1
        self.assertEqual(
            self.sale_order.order_line.product_uom_qty,
            1,
            "Product quantity should be 1.",
        )

    def test_sale_order_existing_product_qty_increase(self):
        """Test that the quantity is increased for an existing product in the sale order"""

        # scan the barcode to create the line
        with Form(self.sale_order) as form:
            form._barcode_scanned = "12345"  # scan method
            form.save()  # save the form to apply the barcode scan

        # check that the order now has one line and the quantity is 1
        self.assertEqual(
            len(self.sale_order.order_line),
            1,
            "Sale order should have 1 line after first scan.",
        )
        self.assertEqual(
            self.sale_order.order_line.product_uom_qty,
            1,
            "Product quantity should be 1 after first scan.",
        )

        # scan the same barcode again to increase quantity
        with Form(self.sale_order) as form:
            form._barcode_scanned = "12345"  # second scan
            form.save()  # Save the form to apply the barcode scan

        # check if qty increased to 2
        self.assertEqual(
            self.sale_order.order_line.product_uom_qty,
            2,
            "Product quantity should be 2 after second scan.",
        )

    def test_sale_order_invalid_product(self):
        """Test that a ValidationError is raised when a barcode does not match any product"""
        with self.assertRaises(ValidationError):
            self.sale_order.on_barcode_scanned("invalid_barcode")
