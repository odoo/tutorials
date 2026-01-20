from odoo.exceptions import UserError

from odoo.fields import Command
from odoo.tests.common import tagged, TransactionCase


@tagged('post_install', '-at_install')
class TestZeroStockBlockage(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group_sale_manager = cls.env.ref('sales_team.group_sale_manager').id
        cls.group_sale_user = cls.env.ref('sales_team.group_sale_salesman').id

        cls.sale_user = cls.env['res.users'].create({
            'name': 'Sale User1',
            'login': 'sale_user1',
            'email': 'saleuser1@example.com',
            'groups_id': [(6, 0, [cls.group_sale_user])],
        })

        cls.sale_manager = cls.env['res.users'].create({
            'name': 'Sale Manager1',
            'login': 'sale_manager1',
            'email': 'salemanager1@example.com',
            'groups_id': [(6, 0, [cls.group_sale_manager])],
        })

        cls.partner1 = cls.env['res.partner'].create({'name': 'Test Partner1'})

        cls.product_template_zero_stock = cls.env['product.template'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'standard_price': 80.0,
            'type': 'consu',
        })

        cls.product_zero_stock = cls.product_template_zero_stock.product_variant_id

        cls.sale_order_zero_stock = cls.env['sale.order'].create({
            'partner_id': cls.partner1.id,
            'user_id': cls.sale_user.id,
            'order_line': [
                Command.create({
                    'product_id': cls.product_zero_stock.id,
                    'product_uom_qty': 2,
                }),
            ],
        })

        cls.product_template_available_stock = cls.env['product.template'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'standard_price': 80.0,
            'type': 'consu',
        })

        cls.product_available_stock = cls.product_template_available_stock.product_variant_id

        cls.sale_order_available_stock = cls.env['sale.order'].create({
            'partner_id': cls.partner1.id,
            'user_id': cls.sale_user.id,
            'order_line': [
                Command.create({
                    'product_id': cls.product_available_stock.id,
                    'product_uom_qty': 1,
                }),
            ],
        })

    def test_sale_order_confirmation_with_zero_stock(self):
        sale_order = self.sale_order_zero_stock
        product = self.product_zero_stock

        product.qty_available = 0
        self.assertEqual(product.qty_available, 0, "Product should have zero stock for this test.")

        with self.assertRaises(UserError, msg="Agent should not be able to confirm this sale order without approval."):
            sale_order.with_user(self.sale_user).action_confirm()

        sale_order.with_user(self.sale_manager).write({'zero_stock_approval': True})
        self.assertTrue(sale_order.zero_stock_approval, "Approval should be True after manager approval.")

        sale_order.with_user(self.sale_user).action_confirm()
        self.assertEqual(sale_order.state, 'sale', "Sale order should be confirmed after approval.")

    def test_sale_order_confirmation_with_available_stock(self):
        sale_order = self.sale_order_available_stock

        self.product_available_stock.qty_available = 100

        self.assertFalse(sale_order.zero_stock_approval, "Default approval should be False.")

        sale_order.with_user(self.sale_user).action_confirm()
        self.assertEqual(sale_order.state, 'sale', "Sale order should be confirmed without approval for this sale order.")
