from odoo import Command, fields
from odoo.addons.l10n_in.tests.common import L10nInTestInvoicingCommon
from odoo.tests import tagged


@tagged('post_install', '-at_install', 'post_install_l10n')
class TestZeroQuantityField(L10nInTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.invoice = cls.init_invoice('out_invoice', cls.partner_a)

        cls.invoice_line = cls.env['account.move.line'].create({
            'move_id': cls.invoice.id,
            'product_id': cls.product_a.id,
            'quantity': 10,
            'price_unit': 100,
            'l10n_in_is_zero_quantity': False
        })

    def test_l10n_in_zero_quantity_field(self):
        """
        Test that the 'l10n_in_is_zero_quantity' field sets the quantity to zero
        in EDI line details.
        """
        # Ensure quantity is not zero by default
        edi_format = self.env['account.edi.format'].search([('name', 'ilike', 'Invoice')])

        line_details = edi_format._get_l10n_in_edi_line_details(0, self.invoice_line, {})
        self.assertNotEqual(line_details['Qty'], 0)

        # Set the zero quantity field and check again
        self.invoice_line.l10n_in_is_zero_quantity = True
        line_details = edi_format._get_l10n_in_edi_line_details(0, self.invoice_line, {})
        self.assertEqual(line_details['Qty'], 0)

    def test_invoice_workflow_with_zero_quantity(self):
        """
        Full workflow test: Create, validate invoice and ensure the zero quantity
        behavior is consistent throughout.
        """
        self.invoice_line.l10n_in_is_zero_quantity = True

        # Validate invoice
        self.invoice.action_post()
        self.assertEqual(self.invoice.state, 'posted')

        # Ensure quantity remains zero in EDI line details
        edi_format = self.env['account.edi.format'].search([('name', 'ilike', 'Invoice')])
        line_details = edi_format._get_l10n_in_edi_line_details(0, self.invoice_line, {})
        self.assertEqual(line_details['Qty'], 0)
