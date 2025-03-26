from odoo.tests import tagged
from odoo.tests.common import TransactionCase

@tagged('post_install', '-at_install')
class TestPosReceiptLayout(TransactionCase):
    @classmethod
    def setUpClass(self):
        """Setup test environment"""
        super(TestPosReceiptLayout, self).setUpClass()
        
        self.pos_config = self.env['pos.config'].create({
            'name': 'Test POS Config',
            'receipt_layout': 'light',
            'receipt_logo': False,
            'receipt_header': '<p>Welcome to My Store</p>',
            'receipt_footer': '<p>Thank You for Shopping!</p>'
        })
        self.receipt_layout = self.env['pos.receipt.layout'].create({
            'pos_config_id': self.pos_config.id
        })

    def test_light_template_rendering(self):
        """Test that the light receipt template is loaded correctly"""
        self.receipt_layout.pos_config_id.receipt_layout = 'light'
        self.receipt_layout._compute_receipt_preview()
        rendered_template = self.receipt_layout.receipt_preview
        self.assertIn('Welcome to My Store', rendered_template, "Header is missing in Light temFalseplate")
        self.assertIn('Thank You for Shopping!', rendered_template, "Footer is missing in Light template")

    def test_boxed_template_rendering(self):
        """Test that the boxed receipt template is loaded correctly"""
        self.receipt_layout.pos_config_id.receipt_layout = 'boxes'
        self.receipt_layout._compute_receipt_preview()
        rendered_template = self.receipt_layout.receipt_preview
        self.assertIn('Welcome to My Store', rendered_template, "Header is missing in Boxed template")
        self.assertIn('Thank You for Shopping!', rendered_template, "Footer is missing in Boxed template")

    def test_lined_template_rendering(self):
        """Test that the lined receipt template is loaded correctly"""
        self.receipt_layout.pos_config_id.receipt_layout = 'lined'
        self.receipt_layout._compute_receipt_preview()
        rendered_template = self.receipt_layout.receipt_preview
        self.assertIn('Welcome to My Store', rendered_template, "Header is missing in Lined template")
        self.assertIn('Thank You for Shopping!', rendered_template, "Footer is missing in Lined template")
