from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class LastOrderedProductsTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.test_product_1 = cls.env['product.product'].create({
            'name': 'New_Product_1',
            'purchase_method': 'purchase'
        })
        cls.test_product_2 = cls.env['product.product'].create({
            'name': 'New_Product_2',
            'purchase_method': 'purchase'
        })
        cls.test_product_3 = cls.env['product.product'].create({
            'name': 'New_Product_3',
            'purchase_method': 'purchase'
        })
        cls.test_product_4 = cls.env['product.product'].create({
            'name': 'New_Product_4',
            'purchase_method': 'purchase'
        })

        cls.test_partner_1 = cls.env['res.partner'].create({
            'name': 'new_partner'
        })

        cls.test_journal_type_sale = cls.env['account.journal'].search([
            ('type', '=', 'sale')
        ], limit=1)

        cls.test_journal_type_purchase = cls.env['account.journal'].search([
            ('type', '=', 'purchase')
        ], limit=1)

        cls.test_sale_order_1 = cls.env['sale.order'].create({
            'partner_id': cls.test_partner_1.id,
            'order_line': [
                (0, 0, {
                    'name': cls.test_product_1.name,
                    'product_id': cls.test_product_1.id,
                    'product_uom_qty': 1,
                    'product_uom': cls.test_product_1.uom_id.id,
                    'price_unit': cls.test_product_1.list_price,
                })
            ],
        })
        cls.test_sale_order_1.action_confirm()
        so_context = {
            'active_model': 'sale.order',
            'active_ids': [cls.test_sale_order_1.id],
            'active_id': cls.test_sale_order_1.id,
            'default_journal_id': cls.test_journal_type_sale.id,
        }
        payment_params = {
            'advance_payment_method': 'percentage',
            'amount': 50,
        }
        cls.test_downpayment = cls.env['sale.advance.payment.inv'].with_context(so_context).create(payment_params)
        cls.test_downpayment.create_invoices()
        cls.test_invoice_1 = cls.env['account.move'].search([
            ('invoice_origin', '=', cls.test_sale_order_1.name)
        ])
        cls.env.cr.execute(""" UPDATE account_move set create_date = '%s' WHERE id = '%s'""" % ('2024-02-10', cls.test_invoice_1.id))

        cls.test_sale_order_2 = cls.env['sale.order'].create({
            'partner_id': cls.test_partner_1.id,
            'order_line': [
                (0, 0, {
                    'name': cls.test_product_2.name,
                    'product_id': cls.test_product_2.id,
                    'product_uom_qty': 1,
                    'product_uom': cls.test_product_2.uom_id.id,
                    'price_unit': cls.test_product_2.list_price,
                })
            ],
        })
        cls.test_sale_order_2.action_confirm()
        so_context = {
            'active_model': 'sale.order',
            'active_ids': [cls.test_sale_order_2.id],
            'active_id': cls.test_sale_order_2.id,
            'default_journal_id': cls.test_journal_type_sale.id,
        }
        payment_params = {
            'advance_payment_method': 'percentage',
            'amount': 50,
        }
        cls.test_downpayment = cls.env['sale.advance.payment.inv'].with_context(so_context).create(payment_params)
        cls.test_downpayment.create_invoices()
        cls.test_invoice_2 = cls.env['account.move'].search([
            ('invoice_origin', '=', cls.test_sale_order_2.name)
        ])
        cls.env.cr.execute(""" UPDATE account_move set create_date = '%s' WHERE id = '%s'""" % ('2023-02-10', cls.test_invoice_2.id))

        cls.test_purchase_order_1 = cls.env['purchase.order'].create({
            'partner_id': cls.test_partner_1.id,
            'order_line': [
                (0, 0, {
                    'name': cls.test_product_3.name,
                    'product_id': cls.test_product_3.id,
                    'product_uom_qty': 1,
                    'product_uom': cls.test_product_3.uom_id.id,
                    'price_unit': cls.test_product_3.list_price,
                })
            ],
        })
        cls.test_purchase_order_1.button_confirm()
        cls.test_purchase_order_1.action_view_picking()
        cls.test_purchase_order_1.action_create_invoice()
        cls.test_bill_1 = cls.env['account.move'].search([
            ('invoice_origin', '=', cls.test_purchase_order_1.name)
        ])
        cls.env.cr.execute(""" UPDATE account_move set create_date = '%s' WHERE id = '%s'""" % ('2024-02-10', cls.test_bill_1.id))

        cls.test_purchase_order_2 = cls.env['purchase.order'].create({
            'partner_id': cls.test_partner_1.id,
            'order_line': [
                (0, 0, {
                    'name': cls.test_product_4.name,
                    'product_id': cls.test_product_4.id,
                    'product_uom_qty': 1,
                    'product_uom': cls.test_product_4.uom_id.id,
                    'price_unit': cls.test_product_4.list_price,
                })
            ],
        })
        cls.test_purchase_order_2.button_confirm()
        cls.test_purchase_order_2.action_view_picking()
        cls.test_purchase_order_2.action_create_invoice()
        cls.test_bill_2 = cls.env['account.move'].search([
            ('invoice_origin', '=', cls.test_purchase_order_2.name)
        ])
        cls.env.cr.execute(""" UPDATE account_move set create_date = '%s' WHERE id = '%s'""" % ('2023-02-10', cls.test_bill_2.id))

    def test_product_variant_in_sale_order(self):
        so_context = {
            'partner_id': self.test_partner_1.id,
            'order_type': 'sale'
        }
        res = self.env['product.product'].with_context(so_context).name_search()
        res_ids = [r[0] for r in res]
        self.assertEqual(self.test_product_1.id, res_ids[0])
        self.assertEqual(self.test_product_2.id, res_ids[1])
        
    def test_product_variant_in_purchase_order(self):
        po_context = {
            'partner_id': self.test_partner_1.id,
            'order_type': 'purchase'
        }
        res = self.env['product.product'].with_context(po_context).name_search()
        res_ids = [r[0] for r in res]
        self.assertEqual(self.test_product_3.id, res_ids[0])
        self.assertEqual(self.test_product_4.id, res_ids[1])
