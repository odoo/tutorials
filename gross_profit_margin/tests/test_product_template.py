from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestProductProduct(TransactionCase):

    def setUp(self):
        super().setUp()
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'lst_price': 150.0,
            'standard_price': 75.0,
        })

    def test_compute_gross_profit_margin(self):
        """Test that gross profit margin is correctly computed"""
        self.product._gross_profit_margin()
        expected_margin = (150.0 - 75.0) / 75.0
        self.assertAlmostEqual(self.product.gross_profit_margin, expected_margin, places=2)

    def test_compute_gross_profit_margin_zero_cost(self):
        """Test that gross profit margin is 0 when standard_price is 0"""
        self.product.standard_price = 0
        self.product._gross_profit_margin()
        self.assertEqual(self.product.gross_profit_margin, 0.0)

    def test_inverse_gross_profit_margin(self):
        """Test that updating gross profit margin updates lst_price correctly"""
        self.product.gross_profit_margin = 0.3
        self.product._inverse_gross_profit_margin()
        expected_lst_price = (self.product.standard_price * 0.3) + self.product.standard_price
        self.assertAlmostEqual(self.product.lst_price, expected_lst_price, places=2)
