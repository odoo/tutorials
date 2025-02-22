from odoo.tests import TransactionCase


class TestSaleOrderLine(TransactionCase):

    def test_compute_book_price(self):
        product = self.env['product.product'].create({
            'name': 'Test Product',
            'lst_price': 150.0,
        })
        sale_order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
        })
        order_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'product_id': product.id,
            'product_uom_qty': 4,
        })

        self.assertEqual(order_line.book_price, 600.0, "Book price should be correctly computed as list_price * quantity.")
