from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestAccountPaymentLines(TransactionCase):

    def setUp(self):
        super(TestAccountPaymentLines, self).setUp()
        
        self.payment_line = self.env['account.payment.lines'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
            'name': 'Test Payment',
            'memo_id': 'INV/2025/001',
            'invoice_date': '2025-03-10',
            'amount_residual': 500.00,
            'balance_amount': 500.00,
            'payment_amount': 200.00,
        })

    def test_valid_payment_amount(self):
        """Test setting a valid payment amount"""
        self.payment_line.write({'payment_amount': 300.00})
        self.assertEqual(self.payment_line.payment_amount, 300.00, "Payment amount should be set correctly.")
        print('===========Test Complete============')

    def test_invalid_payment_amount(self):
        """Test validation when payment amount exceeds balance"""
        with self.assertRaises(ValidationError):
            self.payment_line.write({'payment_amount': 600.00})
        print('===========Test Complete============')
