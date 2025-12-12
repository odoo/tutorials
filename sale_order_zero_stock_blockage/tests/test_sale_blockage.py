from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestSaleZeroStockBlockage(TransactionCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()

        self.sale_user = self.env['res.users'].create({
            'name': 'Salesman Test User',
            'login': 'sales_test_user',
            'email': 'sales_test@example.com',
            'group_ids': [(4, self.env.ref('sales_team.group_sale_salesman').id)],
        })

        self.partner = self.sale_user.partner_id

        self.product_no_stock = self.env['product.product'].create({
            'name': 'Zero Stock Product',
            'type': 'consu',
            'list_price': 100.0,
        })

        self.sale_order = self.env['sale.order'].with_user(self.sale_user).create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product_no_stock.id,
                'product_uom_qty': 1.0,
                'price_unit': 100.0,
            })],
        })

    def test_block_confirm_no_stock(self):
        """ Test that confirming a sale order with zero stock raises an error """
        self.assertEqual(self.product_no_stock.qty_available, 0, "Initial stock should be 0")
        with self.assertRaises(UserError):
            self.sale_order.action_confirm()

    def test_allow_confirm_no_stock(self):
        """ Test that confirming a sale order with zero stock will not raise an error if `zero_stock_approval` is True """
        self.assertEqual(self.product_no_stock.qty_available, 0, "Initial stock should be 0")
        self.sale_order.zero_stock_approval = True
        self.assertEqual(self.sale_order.zero_stock_approval, True, "Cannot comfirm order of insufficent product")
        self.sale_order.action_confirm()

    def test_allow_confirm_with_stock(self):
        """ Test that adding stock allows the order to be confirmed """
        stock_location = self.env.ref('stock.stock_location_stock')
        self.product_no_stock.is_storable = True
        self.env['stock.quant'].create({
            'product_id': self.product_no_stock.id,
            'location_id': stock_location.id,
            'inventory_quantity': 10.0,
        }).action_apply_inventory()
        self.assertEqual(self.product_no_stock.qty_available, 10.0, "Stock should be updated to 10")
        self.sale_order.action_confirm()
        self.assertEqual(self.sale_order.state, 'sale', "Order should be in 'sale' state after confirmation")
