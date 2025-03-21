from odoo.tests import TransactionCase
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged, Form


@tagged("post_install", "-at_install")
class PurchaseOrderInheritTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(PurchaseOrderInheritTestCase, cls).setUpClass()
        # create test products and purchase order for barcode scanning
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "barcode": "12345",
                "list_price": 100.0,
                "type": "consu",
            }
        )

        cls.supplier = cls.env["res.partner"].create(
            {
                "name": "Test Supplier",
            }
        )

        cls.purchase_order = cls.env["purchase.order"].create(
            {
                "partner_id": cls.supplier.id,
                "state": "draft",  # starting with a draft order
            }
        )

        # create a canceled purchase order
        cls.purchase_order_cancelled = cls.env["purchase.order"].create(
            {
                "partner_id": cls.supplier.id,
                "state": "cancel",  # canceled state
            }
        )

        # Create a done (locked) purchase order
        cls.purchase_order_done = cls.env["purchase.order"].create(
            {
                "partner_id": cls.supplier.id,
                "state": "done",  # done state (locked)
            }
        )

    def test_purchase_order_state_cancelled(self):
        """Test that a UserError is raised if trying to scan a barcode on a canceled purchase order"""
        with self.assertRaises(UserError):
            self.purchase_order_cancelled.on_barcode_scanned("12345")
        print("Test 'test_purchase_order_state_cancelled' done!")

    def test_purchase_order_create_line(self):
        """Test that a new line is created when a product is scanned in a draft purchase order"""

        # create the purchase order using form
        with Form(self.purchase_order) as form:
            # scan the barcode (simulating user input)
            form._barcode_scanned = "12345"

            # trigger the barcode scan logic (on_barcode_scanned)
            form.save()

        # check that the order now has one line
        self.assertEqual(
            len(self.purchase_order.order_line),
            1,
            "Purchase order should have 1 line after barcode scan.",
        )

        # ensure the product in the line matches the expected product
        self.assertEqual(
            self.purchase_order.order_line.product_id,
            self.product,
            "Product ID in the order line does not match.",
        )

        # ensure the quantity is correctly set to 1
        self.assertEqual(
            self.purchase_order.order_line.product_uom_qty,
            1,
            "Product quantity should be 1.",
        )

        print("Test 'test_purchase_order_create_line' done!")  # Test passed message

    def test_purchase_order_existing_product_qty_increase(self):
        """Test that the quantity is increased for an existing product in the purchase order"""

        # first scan the barcode to create the line
        with Form(self.purchase_order) as form:
            form._barcode_scanned = "12345"  # simulate the first scan
            form.save()  # save the form to apply the barcode scan

        # check that the order now has one line and the quantity is 1
        self.assertEqual(
            len(self.purchase_order.order_line),
            1,
            "Purchase order should have 1 line after first scan.",
        )
        self.assertEqual(
            self.purchase_order.order_line.product_uom_qty,
            1,
            "Product quantity should be 1 after first scan.",
        )

        # then scan the same barcode again to increase quantity
        with Form(self.purchase_order) as form:
            form._barcode_scanned = "12345"  # simulate the second scan
            form.save()  # save the form to apply the barcode scan

        # check that the quantity has increased to 2
        self.assertEqual(
            self.purchase_order.order_line.product_uom_qty,
            2,
            "Product quantity should be 2 after second scan.",
        )

        print(
            "Test 'test_purchase_order_existing_product_qty_increase' done!"
        )  # test passed message

    def test_purchase_order_invalid_product(self):
        """Test that a ValidationError is raised when a barcode does not match any product"""
        with self.assertRaises(ValidationError):
            self.purchase_order.on_barcode_scanned("invalid_barcode")
        print("Test 'test_purchase_order_invalid_product' done!")  # test passed message

    def test_purchase_order_state_done(self):
        """Test that a UserError is raised if trying to scan a barcode on a locked (done) purchase order"""
        with self.assertRaises(UserError):
            self.purchase_order_done.on_barcode_scanned("12345")
        print("Test 'test_purchase_order_state_done' done!")  # test passed message
