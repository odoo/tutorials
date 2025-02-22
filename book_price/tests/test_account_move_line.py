from odoo.tests import TransactionCase


class TestAccountMoveLine(TransactionCase):

    def test_compute_book_price(self):
        product = self.env['product.product'].create({
            'name': 'Test Product',
            'lst_price': 200.0,
        })
        move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.env.ref('base.res_partner_1').id,
        })
        move_line = self.env['account.move.line'].create({
            'move_id': move.id,
            'product_id': product.id,
            'quantity': 5,
        })

        self.assertEqual(
            move_line.book_price, 1000.0,
            "Book price should be computed correctly as quantity * list_price."
        )
