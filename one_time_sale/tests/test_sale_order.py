from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.sale.tests.common import SaleCommon


@tagged('post_install', '-at_install')
class TestSaleOrder(SaleCommon):
    @classmethod
    def setUpClass(cls):
        """Set up common data for all test cases."""
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Test Customer'})
        cls.plan_monthly = cls.env['sale.subscription.plan'].create({'name': 'Monthly Plan'})
        cls.plan_yearly = cls.env['sale.subscription.plan'].create({'name': 'Yearly Plan'})
        cls.sale_order = cls.env['sale.order'].create({'partner_id': cls.partner.id})

        cls.product_recurring = cls.env['product.product'].create({
            'name': 'Recurring Product ',
            'recurring_invoice': True,
            'type': 'service',
            'list_price': 100.0,
        })
        
        cls.product_recurring2 = cls.env['product.product'].create({
            'name': 'Recurring Product 2',
            'recurring_invoice': True,
            'type': 'consu',
            'list_price': 200.0,
            'product_subscription_pricing_ids': [
                Command.create({'plan_id': cls.plan_monthly.id, 'price': 6}),
                Command.create({'plan_id': cls.plan_yearly.id, 'price': 16}),
            ]
        })

        cls.product_one_time = cls.env['product.product'].create({
            'name': 'One-Time Product',
            'recurring_invoice': False,
            'type': 'consu',
            'list_price': 50.0,
            'accept_one_time': True,
            'product_subscription_pricing_ids': [
                Command.create({'plan_id': cls.plan_monthly.id, 'price': 6}),
                Command.create({'plan_id': cls.plan_yearly.id, 'price': 16}),
            ],
        })

    def test_compute_has_recurring_line(self):
        """Test if sale order detects recurring products correctly."""
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [
                Command.create({
                    'product_id': self.product_recurring.id,
                    'product_uom_qty': 1,
                    'price_unit': self.product_recurring.list_price,
                }),
            ]
        })

        sale_order._compute_has_recurring_line()
        self.assertTrue(sale_order.has_recurring_line, "Sale order should have a recurring product.")

    def test_compute_has_recurring_line_one_time_product(self):
        """Test if sale order detects one time recurring products correctly."""
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [
                Command.create({
                    'product_id': self.product_one_time.id,
                    'product_uom_qty': 1,
                    'price_unit': self.product_one_time.list_price,
                }),
            ]
        })

        sale_order._compute_has_recurring_line()
        self.assertFalse(sale_order.has_recurring_line, "Sale order should not have a recurring product.")

    def test_cart_update_order_line_assign_plan(self):
        """Test assigning a subscription plan when adding a recurring product."""

        # Add a recurring product with a specific plan
        order_line = self.sale_order._cart_update_order_line(
            self.product_recurring.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )
        self.assertEqual(
            self.sale_order.plan_id, self.plan_monthly,
            "Sale order should have the assigned subscription plan.")
        self.assertEqual(
            order_line.product_id,
            self.product_recurring,
            "The order line should contain the recurring product.")

    def test_cart_update_order_line_plan_consistency(self):
        """Test that adding another product does not change the plan_id once set."""
        
        # Add a recurring product with a plan
        self.sale_order._cart_update_order_line(
            self.product_recurring.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )
        
        # Add another recurring product without specifying a plan
        self.sale_order._cart_update_order_line(self.product_recurring2.id, 1, self.env['sale.order.line'])

        self.assertEqual(
            self.sale_order.plan_id,
            self.plan_monthly,
            "The plan should remain consistent across additions.")

    def test_cart_update_order_line_remove_recurring_product(self):
        """Test removing a recurring product and clearing the subscription plan if no other recurring products exist."""
        
        order_line = self.sale_order._cart_update_order_line(
            self.product_recurring.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )

        self.assertEqual(
            self.sale_order.plan_id,
            self.plan_monthly,
            "Sale order should have the assigned subscription plan.")
        self.assertEqual(
            order_line.product_id,
            self.product_recurring,
            "The order line should contain the recurring product.")

        # Remove the recurring product by setting quantity to 0
        self.sale_order._cart_update_order_line(order_line.product_id.id, 0, order_line)

        self.assertFalse(self.sale_order.plan_id, "Plan ID should be removed when no recurring products remain.")
        self.assertFalse(self.sale_order.order_line, "Order line should be deleted when the product is removed.")

    def test_cart_update_order_line_mix_plans_error(self):
        """Test that adding products with different subscription plans raises an error."""
        
        # Add first recurring product with Monthly Plan
        self.sale_order._cart_update_order_line(
            self.product_recurring.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )

        # Try adding another product with a different plan (Yearly Plan)
        with self.assertRaises(UserError, msg="Should raise error when mixing different subscription plans."):
            self.sale_order._cart_update_order_line(
                self.product_recurring2.id, 1, self.env['sale.order.line'], plan_id=self.plan_yearly.id
            )      

    def test_cart_update_order_line_one_time_product(self):
        """Test that adding a one-time product does not affect the subscription plan."""

        order_line = self.sale_order._cart_update_order_line(
            self.product_recurring2.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )

        self.sale_order._cart_update_order_line(self.product_one_time.id, 1, self.env['sale.order.line'])

        self.assertEqual(
            self.sale_order.plan_id,
            self.plan_monthly,
            "Plan ID should remain unchanged after adding a one-time product.")
        self.assertEqual(
            order_line.price_unit,
            6,
            "Sale order line should contain price_unit as same as monthly plan price.")

    def test_cart_update_order_line_quantity_update(self):
        """Test updating quantity of a recurring product without changing plan_id."""

        order_line = self.sale_order._cart_update_order_line(
            self.product_recurring.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
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

        self.assertEqual(order_line.price_unit, 50.0, "One-time product should retain its default price.")

    def test_cart_update_order_line_subscription_pricing_mixed(self):
        """Test that adding a one-time product does not affect the pricing of a recurring product."""
        
        # Add a subscription product with a monthly plan
        order_line1 = self.sale_order._cart_update_order_line(
            self.product_recurring2.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )

        # Add a one-time product
        order_line2 = self.sale_order._cart_update_order_line(
            self.product_one_time.id, 1, self.env['sale.order.line']
        )

        self.assertEqual(order_line1.price_unit, 6, "Subscription product should follow its pricing rule.")
        self.assertEqual(order_line2.price_unit, 50, "One-time product should retain its standard price.")
        self.assertEqual(self.sale_order.plan_id, self.plan_monthly, "Plan should remain unchanged.")

    def test_cart_update_order_line_remove_recurring_product_with_plan(self):
        """Test removing a recurring product while keeping a one-time product, ensuring plan removal."""
        
        # Add a subscription product
        order_line1 = self.sale_order._cart_update_order_line(
            self.product_recurring2.id, 1, self.env['sale.order.line'], plan_id=self.plan_monthly.id
        )

        # Add a one-time product
        order_line2 = self.sale_order._cart_update_order_line(
            self.product_one_time.id, 1, self.env['sale.order.line']
        )

        # Remove the recurring product
        self.sale_order._cart_update_order_line(order_line1.product_id.id, 0, order_line1)

        self.assertFalse(self.sale_order.plan_id, "Plan ID should be removed when all recurring products are removed.")
        self.assertEqual(order_line2.price_unit, 50, "One-time product should remain unchanged.")

    def test_cart_update_order_line_quantity_update_one_time_product(self):
        """Test updating quantity of a one-time product."""
        
        order_line = self.sale_order._cart_update_order_line(
            self.product_one_time.id, 1, self.env['sale.order.line']
        )

        updated_line = self.sale_order._cart_update_order_line(order_line.product_id.id, 5, order_line)
        self.assertEqual(updated_line.product_uom_qty, 5, "Quantity should be updated correctly.")
        self.assertEqual(updated_line.price_unit, 50, "One-time product price should remain unchanged.")
