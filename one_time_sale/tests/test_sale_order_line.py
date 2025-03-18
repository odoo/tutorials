from odoo.fields import Command
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestSaleOrderLine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.plan_monthly = cls.env['sale.subscription.plan'].create({'name': 'Monthly Plan'})
        cls.plan_yearly = cls.env['sale.subscription.plan'].create({'name': 'Yearly Plan'})

        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'type': 'consu',
            'recurring_invoice': False,
        })
        
        cls.subscription_product = cls.env['product.product'].create({
            'name': 'Subscription Product',
            'list_price': 100.0,
            'type': 'consu',
            'recurring_invoice': True,
            'product_subscription_pricing_ids': [
                Command.create({'plan_id': cls.plan_monthly.id, 'price': 6}),
                Command.create({'plan_id': cls.plan_yearly.id, 'price': 16}),
            ],
        })

        cls.pricelist = cls.env['product.pricelist'].create({
            'name': 'Test Pricelist',
        })

        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.env.ref('base.res_partner_1').id,
            'pricelist_id': cls.pricelist.id,
        })

    def test_pricelist_price_with_recurring_invoice_no_plan(self):
        """Test that the product's list price is returned when it has a recurring invoice and no plan."""
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.subscription_product.id,
        })

        self.assertEqual(sale_order_line.price_unit, 100.0, "List price should be returned when there is no plan.")

    def test_pricelist_price_with_recurring_invoice_with_plan(self):
        """Test that the parent method is called when a subscription plan exists."""
        self.sale_order.plan_id = self.plan_monthly

        sale_order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.subscription_product.id
        })

        self.assertNotEqual(
            sale_order_line.price_unit,
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
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
            'pricelist_id': customer_pricelist.id,
        })

        # Create a sale order line without recurring invoice
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
        })

        # Compute the expected price after 10% discount
        expected_price = self.product.list_price * (1 - 0.10)
        # Call _get_pricelist_price() explicitly and check the price
        computed_price = sale_order_line._get_pricelist_price()

        self.assertEqual(computed_price, expected_price, f"Expected price {expected_price}, but got {computed_price}")

    def test_pricelist_price_fallback_to_price_unit(self):
        """Test that the method returns price_unit if the parent method returns None."""
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'pricelist_item_id': False
        })

        price = sale_order_line._get_pricelist_price()

        self.assertEqual(price, 100.0, "If parent method returns None, price_unit should be returned.")

    def test_price_unit_without_plan(self):
        """Test that a one-time purchase product gets its price from list_price if no plan is set."""
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
        })

        self.assertEqual(
            sale_order_line.price_unit, 
            self.product.list_price, 
            "Without a subscription plan, the price should be the product's list price."
        )

    def test_price_unit_with_plan(self):
        """Test that a subscription product follows plan-based pricing when a plan is applied."""
        self.sale_order.plan_id = self.plan_monthly

        sale_order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.subscription_product.id,
        })

        self.assertEqual(
            sale_order_line.price_unit, 
            6.0, 
            f"With plan_id set, price should be 6.0, but got {sale_order_line.price_unit}."
        )

    def test_price_unit_reset_after_plan_removal(self):
        """Test that removing a plan from sale order resets price to list_price."""
        self.sale_order.plan_id = self.plan_monthly
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.subscription_product.id,
        })

        # Ensure price is set according to the plan
        self.assertEqual(sale_order_line.price_unit, 6.0)
        # Remove the plan
        self.sale_order.plan_id = False

        # Verify price resets to list_price
        self.assertEqual(
            sale_order_line.price_unit,
            self.subscription_product.list_price,
            "After removing plan_id, price should reset to list_price."
        )

    def test_price_unit_change_after_plan_applied(self):
        """Test that applying a plan after adding a one-time purchase product updates the price to the monthly subscription price."""
        
        # Add product to the order (without a plan)
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.subscription_product.id,
        })

        # Ensure the price starts as list_price
        self.assertEqual(
            sale_order_line.price_unit,
            self.subscription_product.list_price,
            "Initially, the price should be the product's list price."
        )

        # Apply a subscription plan
        self.sale_order.plan_id = self.plan_monthly
        # Verify that the price updates to the subscription's monthly price
        self.assertEqual(
            sale_order_line.price_unit,
            6.0,
            "After applying plan_id, the price should update to the monthly subscription price."
        )
