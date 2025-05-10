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


class TestPOSLayoutController(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env['res.users'].create({
            'name': 'Test User',
            'login': 'test_user',
            'email': 'test_user@example.com',
            'password': 'admin',
            'groups_id': [(6, 0, [
                cls.env.ref('base.group_user').id,
                cls.env.ref('point_of_sale.group_pos_user').id
            ])],
        })
        cls.pos_session = cls.env['pos.session'].create({
            'name': 'Test POS Session',
            'user_id': cls.user.id,
            'config_id': cls.env['pos.config'].create({
                'name': 'Test POS Config',
                'pos_disp_type': 'lined',
            }).id,
        })

    def test_get_display_layout(self):
        """Test the /pos/get_display_layout controller."""
        self.authenticate('test_user', 'admin')

        response = self.url_open(
            '/pos/get_display_layout',
            data='{}',
            headers={
                'Content-Type': 'application/json',
            }
        )

        self.assertEqual(response.status_code, 200, "Controller should return a 200 status code.")
        data = response.json()
        self.assertIn('disp_layout', data['result'])
        self.assertEqual(data['result']['disp_layout'], 'lined')