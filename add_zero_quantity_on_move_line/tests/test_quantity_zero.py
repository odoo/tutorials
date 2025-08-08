from odoo.tests import tagged

from odoo.addons.l10n_in.tests.common import L10nInTestInvoicingCommon


@tagged("post_install_l10n", "post_install", "-at_install")
class TestIsZeroQuantityField(L10nInTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.invoice_a = cls.init_invoice(
            move_type='out_invoice',
            partner=cls.partner_a,
        )
        cls.invoice_line_1 = cls.env['account.move.line'].create({
            'move_id': cls.invoice_a.id,
            'product_id': cls.product_a.id,
            'quantity': 5,
            'price_unit': 1,
            'is_zero_quantity': False
        })

    def test_zero_quantity_field(self):
        invoice_line = self.invoice_line_1._get_l10n_in_edi_line_details(0, self.invoice_line_1, {})
        self.assertNotEqual(invoice_line['Qty'], 0)
        self.invoice_line_1.is_zero_quantity = True
        invoice_line = self.invoice_line_1._get_l10n_in_edi_line_details(0, self.invoice_line_1, {})
        self.assertEqual(invoice_line['Qty'], 0)

    def test_Einvoice_for_zero_quantity(self):
        self.invoice_line_1.is_zero_quantity = True
        self.invoice_a.action_post()
        self.assertEqual(self.invoice_a.state, 'posted')
        invoice_line = self.invoice_line_1._get_l10n_in_edi_line_details(0, self.invoice_line_1, {})
        self.assertEqual(invoice_line['Qty'], 0)
