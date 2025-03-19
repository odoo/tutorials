from odoo.tests import tagged

from odoo.addons.one_time_sale.tests.common import TestOneTimeSaleCommon


@tagged('post_install', '-at_install')
class TestProductTemplate(TestOneTimeSaleCommon):
    def test_has_one_time_purchase(self):
        """Test if has_one_time_purchase correctly detects a one-time product in the cart."""
        sale_order = self.env['sale.order'].create({'partner_id': self.partner.id})

        # Add a one-time product to the order
        sale_order._cart_update_order_line(self.product_one_time.id, 1, self.env['sale.order.line'])

        self.assertTrue(
            self.env['product.template'].has_one_time_purchase(sale_order),
            "Sale order should be identified as containing a one-time purchase."
        )

    def test_has_one_time_purchase_without_one_time_purchase(self):
        """Test if has_one_time_purchase correctly detects a one-time product is not in the cart."""
        self.sale_order = self.env['sale.order'].create({'partner_id': self.partner.id})

        # Add a subscription product to the order
        self.sale_order._cart_update_order_line(self.subscription_product.id, 1, self.env['sale.order.line'])

        self.assertFalse(
            self.env['product.template'].has_one_time_purchase(self.sale_order),
            "Sale order should be identified as not containing a one-time purchase product."
        )
