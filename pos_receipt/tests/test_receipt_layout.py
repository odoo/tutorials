from odoo.tests.common import TransactionCase

class TestReceiptsLayout(TransactionCase):
    def setUp(self):
        super().setUp()
        self.pos_config = self.env['pos.config'].create({
            'name': 'Test POS',
            'receipt_layout': 'light',
            'receipt_header': 'Header Test',
            'receipt_footer': 'Footer Test',
            'receipt_logo': False,
        })

    def test_default_pos_config(self):
        """Test that the wizard initializes with the correct POS config."""
        wizard = self.env['receipts.layout'].with_context(active_pos_config_id=self.pos_config.id).create({})
        self.assertEqual(wizard.pos_config_id, self.pos_config)

    def test_receipt_preview_computation(self):
        """Test that receipt preview is correctly computed based on layout and fields."""
        wizard = self.env['receipts.layout'].create({'pos_config_id': self.pos_config.id})
        wizard._compute_receipt_preview()
        self.assertTrue(isinstance(wizard.preview, str))

    def test_receipt_layout_selection(self):
        """Test receipt layout template selection based on retail mode."""
        wizard = self.env['receipts.layout'].create({'pos_config_id': self.pos_config.id, 'receipt_layout': 'boxes'})
        template = wizard._get_receipt_preview_template()
        self.assertEqual(template, 'pos_receipt.report_receipts_wizard_preview_boxes')
        
        wizard.receipt_layout = 'lined'
        template = wizard._get_receipt_preview_template()
        self.assertEqual(template, 'pos_receipt.report_receipts_wizard_preview_lined')
        wizard.receipt_layout = 'light'
        template = wizard._get_receipt_preview_template()
        self.assertEqual(template, 'pos_receipt.report_receipts_wizard_preview_light')

    def test_receipt_layout_selection_restaurant(self):
        """Test receipt layout template selection for restaurant mode."""
        self.pos_config.module_pos_restaurant = True
        wizard = self.env['receipts.layout'].create({'pos_config_id': self.pos_config.id, 'receipt_layout': 'boxes'})
        template = wizard._get_receipt_preview_template()
        self.assertEqual(template, 'pos_receipt.report_restaurant_preview_boxes')
        
        wizard.receipt_layout = 'lined'
        template = wizard._get_receipt_preview_template()
        self.assertEqual(template, 'pos_receipt.report_restaurant_preview_lined')
        
        wizard.receipt_layout = 'light'
        template = wizard._get_receipt_preview_template()
        self.assertEqual(template, 'pos_receipt.report_restaurant_preview_light')

    def test_receipt_layout_save(self):
        """Test that saving the wizard closes the window."""
        wizard = self.env['receipts.layout'].create({'pos_config_id': self.pos_config.id})
        result = wizard.receipt_layout_save()
        self.assertEqual(result.get('type'), 'ir.actions.act_window_close')
