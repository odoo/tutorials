import logging
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class TestSaleOrder(TransactionCase):

    def setUp(self):
        """Set up test records before running test cases."""
        super(TestSaleOrder, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer'
        })
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'original_promise_date': '2024-03-15',
            'revised_promise_date': '2024-03-15',
        })
        _logger.info("\n✅ Setup: Sale Order Created Successfully")

    def test_sale_order_creation(self):
        """Test if a Sale Order is created successfully."""
        self.assertTrue(self.sale_order, "Sale Order should be created.")
        self.assertEqual(str(self.sale_order.original_promise_date), '2024-03-15')
        _logger.info("\n✅ Test Passed: Sale Order Creation")

    def test_original_promise_date_required(self):
        """Test that a Sale Order cannot be confirmed without an Original Promise Date."""
        self.sale_order.original_promise_date = False
        with self.assertRaises(ValidationError):
            self.sale_order.action_confirm()
        _logger.info("\n✅ Test Passed: Original Promise Date Required for Confirmation")

    def test_original_promise_date_readonly_after_confirmation(self):
        """Test that Original Promise Date cannot be changed after order is confirmed."""
        self.sale_order.action_confirm()
        with self.assertRaises(ValidationError):
            self.sale_order.write({'original_promise_date': '2024-03-20'})
        _logger.info("\n✅ Test Passed: Original Promise Date Cannot be Modified After Confirmation")

    def test_revised_promise_date_defaults(self):
        """Test that `revised_promise_date` defaults to `original_promise_date` if empty."""
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'original_promise_date': '2024-04-01',
            'revised_promise_date': None, 
        })
        self.assertEqual(str(sale_order.revised_promise_date), '2024-04-01', 
                        "Revised Promise Date should default to Original Promise Date")
        _logger.info("\n✅ Test Passed: Revised Promise Date Defaults to Original Promise Date")

    def test_revised_promise_date_change_logs_history(self):
        """Test if changing `revised_promise_date` logs it in the history table."""
        old_date = self.sale_order.revised_promise_date
        new_date = '2024-03-20'
        self.sale_order.write({'revised_promise_date': new_date})
        history_record = self.env['promise.date.record'].search([
            ('sale_order_id', '=', self.sale_order.id)
        ], order="id desc", limit=1)
        self.assertEqual(str(history_record.from_date), str(old_date))
        self.assertEqual(str(history_record.to_date), new_date)
        _logger.info("\n✅ Test Passed: Revised Promise Date Change Logged in History")

    def test_promise_date_record_creation(self):
        """Test that a promise date record is created when revised_promise_date changes."""
        self.sale_order.write({'revised_promise_date': '2024-03-25'})
        history_record = self.env['promise.date.record'].search([
            ('sale_order_id', '=', self.sale_order.id)
        ], order="id desc", limit=1)
        self.assertTrue(history_record, "A promise date record should be created.")
        self.assertEqual(str(history_record.to_date), '2024-03-25')
        _logger.info("\n✅ Test Passed: Promise Date Record Created")
