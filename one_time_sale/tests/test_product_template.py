from odoo.fields import Command
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestProductTemplate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        """Set up common test data."""
        super().setUpClass()

        cls.partner = cls.env['res.partner'].create({'name': 'Test Customer'})
        cls.plan_monthly = cls.env['sale.subscription.plan'].create({'name': 'Monthly Plan'})
        cls.plan_yearly = cls.env['sale.subscription.plan'].create({'name': 'Yearly Plan'})

        cls.product_one_time = cls.env['product.product'].create({
            'name': 'Recurring Consumable',
            'recurring_invoice': True,
            'type': 'consu',
            'list_price': 200.0,
            'accept_one_time': True,
            'product_subscription_pricing_ids': [
                Command.create({'plan_id': cls.plan_monthly.id, 'price': 6}),
                Command.create({'plan_id': cls.plan_yearly.id, 'price': 16}),
            ],
        })

    def test_has_one_time_purchase(self):
        """Test if has_one_time_purchase correctly detects a one-time product in the cart."""
        sale_order = self.env['sale.order'].create({'partner_id': self.partner.id})

        # Add a one-time product to the order
        sale_order._cart_update_order_line(self.product_one_time.id, 1, self.env['sale.order.line'])

        self.assertTrue(
            self.env['product.template'].has_one_time_purchase(sale_order),
            "Sale order should be identified as containing a one-time purchase."
        )
