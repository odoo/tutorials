from odoo.fields import Command
from odoo.tests import tagged
from odoo.exceptions import UserError

from odoo.addons.one_time_sale.tests.common import TestOneTimeSaleCommon


@tagged('post_install', '-at_install')
class TestSaleOrder(TestOneTimeSaleCommon):
    @classmethod
    def setUpClass(cls):
        """Set up common data for all test cases."""
        super().setUpClass()

        cls.sale_order_with_subscription_product = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'order_line': [
                Command.create({
                    'product_id': cls.subscription_product.id,
                    'product_uom_qty': 1,
                    'price_unit': cls.subscription_product.list_price,
                }),
            ]
        })

        cls.sale_order_with_one_time_purchase = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'order_line': [
                Command.create({
                    'product_id': cls.product_one_time.id,
                    'product_uom_qty': 1,
                    'price_unit': cls.product_one_time.list_price,
                }),
            ]
        })

        cls.subscription_product2 = cls.env['product.product'].create({
            'name': 'Recurring Consumable 2',
            'recurring_invoice': True,
            'type': 'consu',
            'list_price': 100.0,
            'product_subscription_pricing_ids': [
                Command.create({'plan_id': cls.plan_monthly.id, 'price': 6.0}),
                Command.create({'plan_id': cls.plan_yearly.id, 'price': 16.0}),
            ],
        })

    def test_compute_has_recurring_line(self):
        """Test if sale order detects recurring products correctly."""
        self.sale_order_with_subscription_product._compute_has_recurring_line()
        self.assertTrue(
            self.sale_order_with_subscription_product.has_recurring_line,
            "Sale order should have a recurring product.")

    def test_compute_has_recurring_line_one_time_product(self):
        """Test if sale order detects one time recurring products correctly."""
        self.sale_order_with_one_time_purchase._compute_has_recurring_line()
        self.assertFalse(
            self.sale_order_with_one_time_purchase.has_recurring_line,
            "Sale order should not have a recurring product.")

    def test_cart_update_order_line_assign_plan(self):
        """Test assigning a subscription plan when adding a recurring product."""

        # Add a recurring product with a specific plan
        order_line = self.sale_order._cart_update_order_line(
            self.subscription_product.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )

        self.assertEqual(
            self.sale_order.plan_id, self.plan_monthly,
            "Sale order should have the assigned subscription plan.")
        self.assertEqual(
            order_line.product_id,
            self.subscription_product,
            "The order line should contain the recurring product.")

    def test_cart_update_order_line_plan_consistency(self):
        """Test that adding another product does not change the plan_id once set."""
        # Add a recurring product with a plan
        self.sale_order._cart_update_order_line(
            self.subscription_product.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )

        # Add another recurring product without specifying a plan
        self.sale_order._cart_update_order_line(self.subscription_product2.id, 1, self.env['sale.order.line'])

        self.assertEqual(
            self.sale_order.plan_id,
            self.plan_monthly,
            "The plan should remain consistent across additions.")

    def test_cart_update_order_line_remove_recurring_product(self):
        """Test removing a recurring product and clearing the subscription plan if no other recurring products exist."""

        order_line = self.sale_order._cart_update_order_line(
            self.subscription_product.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )

        self.assertEqual(
            self.sale_order.plan_id,
            self.plan_monthly,
            "Sale order should have the assigned subscription plan.")
        self.assertEqual(
            order_line.product_id,
            self.subscription_product,
            "The order line should contain the recurring product.")

        # Remove the recurring product by setting quantity to 0
        self.sale_order._cart_update_order_line(order_line.product_id.id, 0, order_line)

        self.assertFalse(self.sale_order.plan_id, "Plan ID should be removed when no recurring products remain.")
        self.assertFalse(self.sale_order.order_line, "Order line should be deleted when the product is removed.")

    def test_cart_update_order_line_mix_plans_error(self):
        """Test that adding products with different subscription plans raises an error."""

        # Add first recurring product with Monthly Plan
        self.sale_order._cart_update_order_line(
            self.subscription_product.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )

        # Try adding another product with a different plan (Yearly Plan)
        with self.assertRaises(UserError, msg="Should raise error when mixing different subscription plans."):
            self.sale_order._cart_update_order_line(
                self.subscription_product2.id, 1, self.env['sale.order.line'], plan_id=self.plan_yearly.id
            )

    def test_cart_update_order_line_one_time_product(self):
        """Test that adding a one-time product does not affect the subscription plan."""

        order_line = self.sale_order._cart_update_order_line(
            self.subscription_product2.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )

        self.sale_order._cart_update_order_line(self.product_one_time.id, 1, self.env['sale.order.line'])

        self.assertEqual(
            self.sale_order.plan_id,
            self.plan_monthly,
            "Plan ID should remain unchanged after adding a one-time product.")
        self.assertEqual(
            order_line.price_unit,
            6.0,
            "Sale order line should contain price_unit as same as monthly plan price.")

    def test_cart_update_order_line_quantity_update(self):
        """Test updating quantity of a recurring product without changing plan_id."""

        order_line = self.sale_order._cart_update_order_line(
            self.subscription_product.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )

        updated_line = self.sale_order._cart_update_order_line(order_line.product_id.id, 3, order_line)
        self.assertEqual(updated_line.product_uom_qty, 3, "Quantity should be updated correctly.")
        self.assertEqual(
            self.sale_order.plan_id,
            self.plan_monthly,
            "Plan ID should remain the same after quantity update.")

    def test_cart_update_order_line_one_time_product_price(self):
        """Test that a one-time product retains its default price."""

        order_line = self.sale_order._cart_update_order_line(
            self.product_one_time.id, 1, self.env['sale.order.line']
        )

        self.assertEqual(order_line.price_unit, 200.0, "One-time product should retain its default price.")

    def test_cart_update_order_line_subscription_pricing_mixed(self):
        """Test that adding a one-time product does not affect the pricing of a recurring product."""

        # Add a subscription product with a monthly plan
        order_line1 = self.sale_order._cart_update_order_line(
            self.subscription_product2.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )

        # Add a one-time product
        order_line2 = self.sale_order._cart_update_order_line(
            self.product_one_time.id, 1, self.env['sale.order.line']
        )

        self.assertEqual(order_line1.price_unit, 6.0, "Subscription product should follow its pricing rule.")
        self.assertEqual(order_line2.price_unit, 6.0, "One-time product should retain its standard price.")
        self.assertEqual(self.sale_order.plan_id, self.plan_monthly, "Plan should remain unchanged.")

    def test_cart_update_order_line_quantity_update_one_time_product(self):
        """Test updating quantity of a one-time product."""

        order_line = self.sale_order._cart_update_order_line(
            self.product_one_time.id, 1, self.env['sale.order.line']
        )

        updated_line = self.sale_order._cart_update_order_line(order_line.product_id.id, 5, order_line)
        self.assertEqual(updated_line.product_uom_qty, 5, "Quantity should be updated correctly.")
        self.assertEqual(updated_line.price_unit, 200, "One-time product price should remain unchanged.")

    def test_sale_order_without_plan_is_not_subscription(self):
        """Ensure a sale order with a one-time purchase product is NOT considered a subscription."""

        self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_one_time.id,
        })

        self.sale_order._compute_subscription_state()
        self.assertFalse(
            self.sale_order.subscription_state,
            "Sale order should NOT be a subscription when it has only a one-time product."
        )

    def test_sale_order_becomes_subscription_when_plan_is_applied(self):
        """Test that applying a plan to a sale order converts it into a subscription order."""

        self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_one_time.id,
        })

        # Initially, it should not be a subscription order
        self.sale_order._compute_subscription_state()
        self.assertFalse(
            self.sale_order.subscription_state,
            "Sale order should NOT be a subscription before applying a plan."
        )

        # Apply a subscription plan
        self.sale_order.plan_id = self.plan_monthly
        self.sale_order._compute_subscription_state()
        self.assertTrue(
            self.sale_order.subscription_state,
            "Sale order should become a subscription after applying a plan."
        )

    def test_recurring_total_updates_when_plan_is_applied(self):
        """Verify that the recurring total updates correctly after a subscription plan is applied."""

        self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.subscription_product2.id,
        })

        # Apply a subscription plan
        self.sale_order.plan_id = self.plan_monthly
        self.sale_order._compute_subscription_state()

        self.assertEqual(
            self.sale_order.recurring_total,
            6.0,
            "The recurring total should update to match the subscription plan's price."
        )
