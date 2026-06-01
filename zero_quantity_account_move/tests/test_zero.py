from odoo.tests.common import TransactionCase


class TestZeroQuantityEDI(TransactionCase):

    def setUp(self):
        super().setUp()

        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer',
        })

        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'consu',
            'list_price': 20,
        })

    def _get_tax_details(self):
        return {
            'tax_details': {}
        }

    def test_zero_quantity_in_edi(self):

        move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
        })

        self.env['account.move.line'].create({
            'move_id': move.id,
            'product_id': self.product.id,
            'quantity': 9,
            'price_unit': 10,
            'zero_move': True,
            'name': 'Test line',
        })

        move.action_post()
        line = move.invoice_line_ids[0]

        res = move._get_l10n_in_edi_line_details(
            1, line, self._get_tax_details()
        )

        self.assertEqual(res.get('Qty'), 0)

    def test_normal_quantity_in_edi(self):

        move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
        })

        self.env['account.move.line'].create({
            'move_id': move.id,
            'product_id': self.product.id,
            'quantity': 5,
            'price_unit': 100,
            'zero_move': False,
            'name': 'Test line',
        })

        move.action_post()
        line = move.invoice_line_ids[0]

        res = move._get_l10n_in_edi_line_details(
            1, line, self._get_tax_details()
        )

        self.assertEqual(res.get('Qty'), 5)
