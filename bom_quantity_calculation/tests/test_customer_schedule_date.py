from datetime import datetime, timedelta

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestCustomerScheduleDate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner',
        })
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'expected_date': datetime.now() + timedelta(days=5),
        })
        cls.sale_order_line = cls.env['sale.order.line'].create({
            'order_id': cls.sale_order.id,
            'name': 'Test Product',
            'product_id': cls.env['product.product'].create({
                'name': 'Test Product',
                'type': 'consu',
                'list_price': 100.0,
            }).id,
            'product_uom_qty': 1.0,
            'price_unit': 100.0,
        })

    def test_onchange_cust_scheduled_date_error(self):
        """Test that setting cust_scheduled_date earlier than expected_date raises ValidationError."""
        self.sale_order_line.cust_scheduled_date = self.sale_order.expected_date - timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.sale_order_line._onchange_cust_scheduled_date()

    def test_onchange_cust_scheduled_date_success(self):
        """Test that setting cust_scheduled_date later than or equal to expected_date succeeds."""
        valid_date = self.sale_order.expected_date + timedelta(days=1)
        self.sale_order_line.write({'cust_scheduled_date': valid_date})
        self.sale_order_line._onchange_cust_scheduled_date()
        self.assertEqual(self.sale_order_line.cust_scheduled_date, valid_date)
