from odoo import Command
from odoo.tests.common import TransactionCase


class TestOrderOfWork(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'type': 'consu',
            'route_ids': [Command.set([cls.env.ref('purchase_stock.route_warehouse0_buy').id])],
            'seller_ids': [Command.create({
                'partner_id': cls.env['res.partner'].create({'name': 'Test Vendor'}).id,
                'price': 50.0,
                'min_qty': 1,
            })],
            'is_storable': True
        })
        cls.reordering_rule = cls.env['stock.warehouse.orderpoint'].create({
            'product_id': cls.product.id,
            'route_id': cls.env.ref('purchase_stock.route_warehouse0_buy').id,
            'product_min_qty': 10,
            'product_max_qty': 15,
        })
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.env['res.partner'].create({'name': 'Test Customer'}).id,
            'order_of_work': 'Priority Order 1',
        })
        cls.sale_order_line = cls.env['sale.order.line'].create({
            'order_id': cls.sale_order.id,
            'product_id': cls.product.id,
            'product_uom_qty': 1000,
            'price_unit': 50.0,
        })

    def test_order_of_work_purchase_order(self):
        """Test that the `order_of_work` is correctly propagated to purchase orders."""
        self.sale_order.action_confirm()

        purchase_order = self.env['purchase.order'].search([('origin', 'like', self.sale_order.name)], limit=1)

        self.assertTrue(purchase_order)
        self.assertEqual(
            purchase_order.order_of_work,
            self.sale_order.order_of_work
        )

    def test_order_of_work_manufacturing_order(self):
        """Test that the `order_of_work` is correctly propagated to manufacturing orders."""
        self.product.write({'route_ids': [Command.set([self.env.ref('mrp.route_warehouse0_manufacture').id,self.env.ref('stock.route_warehouse0_mto').id])]})
        self.sale_order.action_confirm()

        mo = self.env['mrp.production'].search([('origin', '=', self.sale_order.name)], limit=1)

        self.assertTrue(mo)
        self.assertEqual(
            mo.order_of_work,
            self.sale_order.order_of_work
        )

    def test_order_of_work_multiple_orders(self):
        """Test the functionality in multiple order scenario"""
        product_2 = self.env['product.product'].create({
            'name': 'Test Product 2',
            'type': 'consu',
            'route_ids': [Command.set([self.env.ref('purchase_stock.route_warehouse0_buy').id])],
            'seller_ids': [Command.create({
                'partner_id': self.env['res.partner'].create({'name': 'Test Vendor 2'}).id,
                'price': 50.0,
                'min_qty': 1,
            })],
            'is_storable': True,
            'orderpoint_ids': [Command.create({
                'route_id': self.env.ref('purchase_stock.route_warehouse0_buy').id,
                'product_min_qty': 10,
                'product_max_qty': 15,
            })]
        })
        sale_order_2 = self.env['sale.order'].create({
            'partner_id': self.env['res.partner'].create({'name': 'Test Customer 2'}).id,
            'order_of_work': 'Priority Order 2',
            'order_line': [Command.create({
                'product_id': product_2.id,
                'product_uom_qty': 1000,
                'price_unit': 50.0,
            })],
        })

        sos = self.env['sale.order'].browse([self.sale_order.id, sale_order_2.id])
        sos.action_confirm()
        purchase_orders_1 = self.env['purchase.order'].search([('origin', 'like', self.sale_order.name)])
        purchase_orders_2 = self.env['purchase.order'].search([('origin', 'like', sale_order_2.name)])
        self.assertEqual(purchase_orders_1.order_of_work, self.sale_order.order_of_work)
        self.assertEqual(purchase_orders_2.order_of_work, sale_order_2.order_of_work)
