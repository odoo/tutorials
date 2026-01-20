from odoo.fields import Command
from odoo.tests.common import tagged, TransactionCase


@tagged('post_install', '-at_install')
class TestPricelistPrice(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner1 = cls.env['res.partner'].create({
            'name': 'Test Partner1',
        })

        cls.pricelist = cls.env['product.pricelist'].create({
            'name': 'Test Pricelist',
            'item_ids': [Command.create({
                'compute_price': 'percentage',
                'percent_price': 10,
                'applied_on': '3_global',
            })],
        })

        cls.product_template = cls.env['product.template'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'standard_price': 80.0,
            'type': 'consu',
            'invoice_policy': 'order',
        })

        cls.product = cls.product_template.product_variant_id

    def test_sale_order_with_pricelist(self):
        self.env['ir.config_parameter'].set_param("product.use_pricelists", True)

        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner1.id,
            'pricelist_id': self.pricelist.id,
            'order_line': [
                Command.create({
                    'product_id': self.product.id,
                    'product_uom_qty': 2,        
                }),
            ],
        })

        self.assertEqual(sale_order.order_line.book_price, sale_order.order_line.price_unit, f"Book Price should be {100 - self.pricelist.item_ids.percent_price}% of list price after discount")
        sale_order.order_line.price_unit = 500
        self.assertNotEqual(sale_order.order_line.book_price, sale_order.order_line.price_unit, "Book Price should not be equal to unit price")

        sale_order.action_confirm()
        self.assertEqual(sale_order.state, 'sale', "Sale order should be confirmed successfully")

    def test_sale_order_without_pricelist(self):

        sale_order_no_pricelist = self.env['sale.order'].create({
            'partner_id': self.partner1.id,
            'order_line': [
                Command.create({
                    'product_id': self.product.id,
                    'product_uom_qty': 2,        
                })
            ],
        })

        self.assertEqual(sale_order_no_pricelist.order_line.book_price, sale_order_no_pricelist.order_line.price_unit, "Book Price should be equal to unit price")
        sale_order_no_pricelist.order_line.price_unit = 500
        self.assertNotEqual(sale_order_no_pricelist.order_line.book_price, sale_order_no_pricelist.order_line.price_unit, "Book Price should not be equal to unit price")

    def test_account_move_lines(self):

        sale_order_account_move = self.env['sale.order'].create({
            'partner_id': self.partner1.id,
            'pricelist_id': self.pricelist.id,
            'order_line': [
                Command.create({
                    'product_id': self.product.id,
                    'product_uom_qty': 2,        
                }),
            ],
        })

        sale_order_account_move.action_confirm()
        sale_order_account_move.order_line.qty_delivered = 2

        test_invoice_wizard = self.env['sale.advance.payment.inv'].with_context({
            'active_model': 'sale.order',
            'active_ids': [sale_order_account_move.id],
        }).create({
            'advance_payment_method': 'delivered'
        })

        test_invoice_wizard.create_invoices()

        test_invoice = sale_order_account_move.invoice_ids[0]
        for line in test_invoice.invoice_line_ids:
            line.price_unit = 30
            self.assertNotEqual(line.book_price, line.price_unit, "Book Price should not be equal to unit price")
