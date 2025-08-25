from odoo.tests.common import TransactionCase


class TestPOSConfigureReceipt(TransactionCase):

    def setUp(self):
        super().setUp()
        self.pos_config = self.env['pos.config'].create({
            'name': 'Test POS',
        })

    def test_default_layout(self):
        wizard = self.env['pos.configure.receipt'].create({
            'pos_config_id': self.pos_config.id,
        })
        self.assertEqual(wizard.layout, 'light', "Default layout should be 'light'")

    def test_receipt_preview_render(self):
        wizard = self.env['pos.configure.receipt'].create({
            'pos_config_id': self.pos_config.id,
            'layout': 'boxed',
            'header': '<p>Test Header</p>',
            'footer': '<p>Test Footer</p>',
        })
        wizard._compute_receipt_preview()
        self.assertIn('Test Header', wizard.receipt_preview)
        self.assertIn('Test Footer', wizard.receipt_preview)

    def test_apply_configuration(self):
        wizard = self.env['pos.configure.receipt'].create({
            'pos_config_id': self.pos_config.id,
            'layout': 'lined',
            'header': '<p>Header</p>',
            'footer': '<p>Footer</p>',
        })
        wizard.action_apply_configuration()

        self.assertEqual(self.pos_config.receipt_layout, 'lined')
        self.assertEqual(self.pos_config.receipt_header, 'Header')
        self.assertEqual(self.pos_config.receipt_footer, 'Footer')

        param = self.env['ir.config_parameter'].sudo().get_param('pos.receipt.layout')
        self.assertEqual(param, 'lined')
