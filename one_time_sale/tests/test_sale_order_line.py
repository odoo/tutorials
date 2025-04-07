from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.one_time_sale.tests.common import TestOneTimeSaleCommon


@tagged('post_install', '-at_install')
class TestSaleOrderLine(TestOneTimeSaleCommon):
    @classmethod
    def setUpClass(cls):
        """Set up common test data."""
        super().setUpClass()

        # Create a sale order line
        cls.sale_order_line = cls.env['sale.order.line'].create({
            'order_id': cls.sale_order.id,
            'product_id': cls.product.id,
        })

    def test_pricelist_price_with_recurring_invoice_no_plan(self):
        """Test that the product's list price is returned when it has a recurring invoice and no plan."""
        self.sale_order_line.product_id = self.subscription_product.id

        self.assertEqual(self.sale_order_line.price_unit, 200.0, "List price should be returned when there is no plan.")

    def test_pricelist_price_with_recurring_invoice_with_plan(self):
        """Test that the parent method is called when a subscription plan exists."""
        self.sale_order.plan_id = self.plan_monthly
        self.sale_order_line.product_id = self.subscription_product.id

        self.assertNotEqual(
            self.sale_order_line.price_unit,
            100.0,
            "Price should be computed by the pricelist, not the list price.")

    def test_pricelist_price_without_recurring_invoice(self):
        """Test that the parent method is called when recurring invoice is False and pricelist applies."""
        # Create a pricelist and add an item
        customer_pricelist = self.env['product.pricelist'].create({
            'name': 'Customer Pricelist',
            'item_ids': [
                Command.create({
                    'applied_on': '1_product',
                    'product_tmpl_id': self.product.product_tmpl_id.id,
                    'compute_price': 'formula',
                    'base': 'list_price',
                    'price_discount': 10
                }),
            ],
        })

        # Create a sale order and assign the pricelist
        self.sale_order.pricelist_id = customer_pricelist.id
        # Compute the expected price after 10% discount
        expected_price = self.product.list_price * (1 - 0.10)
        # Call _get_pricelist_price() explicitly and check the price
        computed_price = self.sale_order_line._get_pricelist_price()

        self.assertEqual(computed_price, expected_price, f"Expected price {expected_price}, but got {computed_price}")

    def test_pricelist_price_fallback_to_price_unit(self):
        """Test that the method returns price_unit if the parent method returns None."""
        self.sale_order_line.pricelist_item_id = False
        price = self.sale_order_line._get_pricelist_price()

        self.assertEqual(price, 100.0, "If parent method returns None, price_unit should be returned.")

    def test_price_unit_without_plan(self):
        """Test that a one-time purchase product gets its price from list_price if no plan is set."""
        self.assertEqual(
            self.sale_order_line.price_unit,
            self.product.list_price,
            "Without a subscription plan, the price should be the product's list price."
        )

    def test_price_unit_with_plan(self):
        """Test that a subscription product follows plan-based pricing when a plan is applied."""
        self.sale_order.plan_id = self.plan_monthly
        self.sale_order_line.product_id = self.subscription_product.id

        self.assertEqual(
            self.sale_order_line.price_unit,
            6.0,
            f"With plan_id set, price should be 6.0, but got {self.sale_order_line.price_unit}."
        )

    def test_price_unit_reset_after_plan_removal(self):
        """Test that removing a plan from sale order resets price to list_price."""
        self.sale_order.plan_id = self.plan_monthly
        self.sale_order_line.product_id = self.subscription_product.id

        # Ensure price is set according to the plan
        self.assertEqual(self.sale_order_line.price_unit, 6.0)
        # Remove the plan
        self.sale_order.plan_id = False

        # Verify price resets to list_price
        self.assertEqual(
            self.sale_order_line.price_unit,
            self.subscription_product.list_price,
            "After removing plan_id, price should reset to list_price."
        )

    def test_price_unit_change_after_plan_applied(self):
        """Test that applying a plan after adding a one-time purchase product updates the price to the monthly subscription price."""

        self.sale_order_line.product_id = self.subscription_product.id

        # Ensure the price starts as list_price
        self.assertEqual(
            self.sale_order_line.price_unit,
            self.subscription_product.list_price,
            "Initially, the price should be the product's list price."
        )

        # Apply a subscription plan
        self.sale_order.plan_id = self.plan_monthly
        # Verify that the price updates to the subscription's monthly price
        self.assertEqual(
            self.sale_order_line.price_unit,
            6.0,
            "After applying plan_id, the price should update to the monthly subscription price."
        )
