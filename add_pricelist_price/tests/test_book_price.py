from odoo.tests.common import TransactionCase
from odoo.fields import Command


class TestBookPrice(TransactionCase):

    def setUp(self):
        super().setup()
        Product = self.env['product.product']
        PriceList = self.env['product.pricelist']

        self.product = Product.create({
            'name': 'Test Book',
            'list_price': 100.0,
        })

        self.pricelist = PriceList.create({
            'name': 'Test Pricelist',
            'item_ids': [(Command.create({
               'applied_on': '0_product_variant',
               'product_id': self.product.id,
               'compute_price': 'formula',
               'base': 'list_price',
               'price_discount': 20.0
            }))],
        })
        self.partner=self.env['res.partner'].create({
            'name': 'Test Partner',
        })

    def test_book_price_on_sale_order_line(self):
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'pricelist_id': self.pricelist.id,
            'order_line': [Command.create({
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'price_unit': 100.0
            })]
        })

        line = sale_order.order_line[0]
        line._compute_price()
        self.assertAlmostEqual(
            line.book_price,
            80.0,
            places=2,
            msg="Book price should be 80.0 after applying 20% discount on list price of 100.0"
        )

    def test_book_price_fallback_to_list_price(self):
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [Command.create({
                'product_id':self.product.id,
                'product_umo_qty':1,
                'price_unit':100.0,
            })]
        })
        line = sale_order.order_line[0]
        line._compute_price()
        self.assertEqual(
            line.book_price,
            self.product.list_price,
            "Book price should fallback to list price when no pricelist is applied"
        )

    def test_book_price_on_customer_invoice_line(self):
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'pricelist_id': self.pricelist.id,
            'order_line': [Command.create({
                'product_id':self.product.id,
                'product_uom_qty':2,
                'price_unit':200.0,
            })]
        })
        sale_order.action_confirm()
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'invoice_line_ids': [Command.create({
                'product_id':self.product.id,
                'invoice_line_ids': [Command.create({
                    'product_id': self.product.id,
                    'quantity': 2,
                    'price_unit': 200.0,
                    'sale_line_ids': [(6, 0, [sale_order.order_line.id])],
                })]
            })]
        })
        line = invoice.invoice_line_ids[0]
        line._compute_book_price()
        self.assertAlmostEqual(
        line.book_price,
        80.0,
        places=2,
        msg="Invoice line book price should come from the sale order pricelist"
        )

    def test_book_price_not_show_on_non_out_invoice(self):
        invoice = self.env['account.move'].create({
            'move_type': 'out_refund',
            'partner_id': self.partner.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 100.0,
            })],
        })

        line = invoice.invoice_line_ids[0]
        line._compute_book_price()
        self.assertEqual(
            line.book_price,
            self.product.list_price,
            "Book price should be computed but hidden in UI for non-customer-invoice types"
        )
