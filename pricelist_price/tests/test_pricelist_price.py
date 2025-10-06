from odoo import Command
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install', 'pricelist_test')
class TestPricelistPrice(TransactionCase):
    def setUp(self):
        super().setUp()
        self.my_pricelist = self.env['product.pricelist'].create({
            'name': 'test_pricelist',
            'item_ids': [Command.create({
                'compute_price': 'percentage',
                'percent_price': 10,
                'applied_on': '3_global'
            })],
        })
        self.test_product = self.env['product.product'].create({
            'name': 'T-Shirt',
            'type': 'consu',
            'list_price': 20.0,
            'invoice_policy': 'order',
        })
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
            'pricelist_id': self.my_pricelist.id, 
            'order_line': [(0, 0, {
                'product_id': self.test_product.id,
                'product_uom_qty': 1,
            })]
        })

    def test_book_price(self):
        order_line = self.sale_order.order_line
        self.assertEqual(order_line.book_price, order_line.price_unit, "book_price should initially match price_unit")
        order_line.price_unit = 100
        self.assertNotEqual(order_line.book_price, order_line.price_unit, "book_price should not change when price_unit is modified")

    def test_account_book_price(self):
        self.sale_order.action_confirm()
        invoice_wizard = self.env['sale.advance.payment.inv'].with_context({
            'active_model': 'sale.order',
            'active_ids': [self.sale_order.id],
        }).create({
            'advance_payment_method': 'delivered'
        })
        invoice_wizard.create_invoices()
        invoice = self.sale_order.invoice_ids[0]

        for line in invoice.invoice_line_ids:
            original_book_price = line.book_price
            line.price_unit = 30
            self.assertEqual(line.book_price, original_book_price, "book_price should not change even if price_unit is modified")
