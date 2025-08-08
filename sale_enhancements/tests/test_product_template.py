from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class LastSoldProducts(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product_1 = cls.env['product.product'].create({
            'name': 'Test Product 1',
        })
        cls.partner_1 = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'test@example.com',
        })
        cls.test_journal_type_sale = cls.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        cls.sale_order_1 = cls.env['sale.order'].create({
            'partner_id': cls.partner_1.id,
            'order_line': [(0, 0, {
                'product_id': cls.product_1.id,
                'product_uom_qty': 1,
                'product_uom': cls.product_1.uom_id.id,
                'price_unit': cls.product_1.lst_price,
            })],
        })
        cls.sale_order_1.action_confirm()
        so_context = {
            'active_model': 'sale.order',
            'active_ids': [cls.sale_order_1.id],
            'active_id': cls.sale_order_1.id,
            'default_journal_id': cls.test_journal_type_sale.id,
        }
        downpayment = cls.env['sale.advance.payment.inv'].with_context(so_context).create({
            'advance_payment_method': 'percentage',
            'amount': 50,
        })
        downpayment.create_invoices()
        invoice = cls.env['account.move'].search([
            ('invoice_origin', '=', cls.sale_order_1.name)
        ], limit=1)
        if not invoice:
            raise ValueError("Invoice was not created for Sale Order 1.")
        invoice.write({'create_date': '2025-01-10 10:00:00'})
        cls.env.invalidate_all()

    def test_single_product_appears_in_name_search(self):
        """Test that a single invoiced product appears in name_search with context."""
        context = {
            'partner_id': self.partner_1.id,
            'order_type': 'sale'
        }
        result = self.env['product.product'].with_context(context).name_search(
            name='', args=[('id', '=', self.product_1.id)]
        )
        self.assertTrue(result, "Product 1 should be returned in name_search result.")
        self.assertEqual(result[0][0], self.product_1.id, "Returned product should be Product 1.")
