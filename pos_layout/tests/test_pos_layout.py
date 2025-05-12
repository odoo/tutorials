from odoo.tests.common import TransactionCase, HttpCase
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestPOSReceiptPreviewWizard(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company

        cls.pos_config = cls.env['pos.config'].create({
            'name': 'Test PoS'
        })

        cls.settings_config = cls.env['res.config.settings'].create({
            'pos_config_id': cls.pos_config.id
        })

        cls.wizard = cls.env['pos.receipt.preview.wizard'].with_context(
            active_id=cls.settings_config.id
        ).create({})

    def test_default_get(self):
        self.assertEqual(self.wizard.pos_disp_type, "default", "Default layout should be set correctly")
        self.assertEqual(self.wizard.receipt_header, self.pos_config.receipt_header, "Receipt header should be correctly fetched")
        self.assertEqual(self.wizard.receipt_footer, self.pos_config.receipt_footer, "Receipt footer should be correctly fetched")
        self.assertEqual(self.wizard.logo_image, self.company.logo, "Logo should be fetched from company settings")

    def test_compute_preview(self):
        self.wizard.receipt_header = "Test Header"
        self.wizard.receipt_footer = "Test Footer"

        self.wizard._compute_preview()

        self.assertIn("Test Header", self.wizard.preview, "Preview should contain the updated header")
        self.assertIn("Test Footer", self.wizard.preview, "Preview should contain the updated footer")

    def test_action_confirm(self):
        self.wizard.receipt_header = "Confirmed Header"
        self.wizard.receipt_footer = "Confirmed Footer"
        self.wizard.pos_disp_type = "boxed"

        self.wizard.action_confirm()

        self.assertEqual(self.settings_config.pos_config_id.pos_disp_type, self.wizard.pos_disp_type, "POS Display type is not set perfectly")
        self.assertEqual(self.settings_config.pos_config_id.receipt_header, self.wizard.receipt_header, "Disp header is not set correctly")
        self.assertEqual(self.settings_config.pos_config_id.receipt_footer, "Confirmed Footer", "Receipt footer should be saved")
        self.assertEqual(self.company.logo, self.wizard.logo_image, "Company logo should be updated")
