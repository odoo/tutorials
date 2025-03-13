from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError

class TestSaleOrderApproval(TransactionCase):

    def setUp(self):
        """Setup test data for sale order and approval category."""
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "Test Customer"})
        self.product = self.env["product.product"].create({
            "name": "Test Product",
            "list_price": 1000
        })
        self.approval_category = self.env["approval.category"].create({
            "name": "Sales Approval",
            "is_sales_approval": True,
            "from_amount": 500,
            "to_amount": 10000
        })
        self.sale_order = self.env["sale.order"].create({
            "partner_id": self.partner.id,
            "order_line": [(0, 0, {
                "product_id": self.product.id,
                "product_uom_qty": 1,
                "price_unit": 1000
            })]
        })

    def test_sent_for_approval_success(self):
        """Test that order can be sent for approval successfully."""
        self.sale_order.action_sent_for_approval()
        self.assertTrue(self.sale_order.approval_request_id, "Approval request was not created.")

    def test_sent_for_approval_without_product(self):
        """Test that sending an order without products raises ValidationError."""
        empty_order = self.env["sale.order"].create({"partner_id": self.partner.id})
        with self.assertRaises(ValidationError, msg="You cannot send an empty order for approval."):
            empty_order.action_sent_for_approval()

    def test_sent_for_approval_twice_after_approval(self):
        """Test that sending an already approved order raises UserError."""
        self.sale_order.action_sent_for_approval()
        self.sale_order.approval_request_id.request_status = "approved"
        with self.assertRaises(UserError, msg="This order is already approved. No need to send again."):
            self.sale_order.action_sent_for_approval()

    def test_confirm_order_after_approval(self):
        """Test that order gets confirmed after approval."""
        self.sale_order.action_sent_for_approval()
        self.sale_order.approval_request_id.request_status = "approved"
        self.sale_order.action_confirm()
        self.assertEqual(self.sale_order.state, "sale", "Sale order was not confirmed after approval.")

    def test_confirm_order_without_approval(self):
        """Test that confirming an order without approval raises UserError."""
        with self.assertRaises(UserError, msg="Order must be sent for approval and fully approved before confirmation."):
            self.sale_order.action_confirm()

    def test_confirm_order_when_approval_is_pending(self):
        """Test that confirming an order when approval is pending raises UserError."""
        self.sale_order.action_sent_for_approval()
        self.sale_order.approval_request_id.request_status = "pending"
        with self.assertRaises(UserError, msg="Order must be sent for approval and fully approved before confirmation."):
            self.sale_order.action_confirm()
