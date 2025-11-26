from odoo.tests import tagged, common

@tagged('post_install', '-at_install') 
class TestSaleWarranty(common.TransactionCase):

    def setUp(self):
        super().setUp()
        # Create demo data
        self.product_warranty = self.env['product.template'].create({
            'name': 'Warranty Product',
            'is_warranty': True,
        })
        self.product_non_warranty = self.env['product.template'].create({
            'name': 'Non Warranty Product',
            'is_warranty': False,
        })
        self.warranty_config = self.env['product.warranty.configuration'].create({
            'name': 'New Year Warranty',
            'product_id': self.product_warranty.id,
            'percentage': 10.0,
            'years': 1,
        })
        self.customer = self.env['res.partner'].create({'name': 'Test Customer'})
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.customer.id,
        })
        self.sale_order_line_non_warranty = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_non_warranty.product_variant_id.id,
            'product_uom_qty': 2,
            'price_unit': 100,
        })
        self.sale_order_line_warranty = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_warranty.product_variant_id.id,
            'product_uom_qty': 1,
            'price_unit': 50,
        })

    def test_warranty_wizard_initialization(self):
        # Test default_get of the warranty wizard
        self.sale_order.write({'order_line': [
            (1, self.sale_order_line_non_warranty.id, {'product_id': self.product_non_warranty.product_variant_id.id}),
            (1, self.sale_order_line_warranty.id, {'product_id': self.product_warranty.product_variant_id.id}),
        ]})
        wizard = self.env['product.add.warranty'].with_context(active_id=self.sale_order.id).create({})
        self.assertEqual(wizard.order_id, self.sale_order)
        self.assertEqual(len(wizard.warranty_line_ids), 1)
        self.assertEqual(wizard.warranty_line_ids.order_line_id, self.sale_order_line_warranty)

    def test_warranty_added_when_selected(self):
        #Test that a warranty line is correctly added 
        wizard = self.env['product.add.warranty'].with_context(active_id=self.sale_order.id).create({})
        self.assertTrue(wizard.warranty_line_ids, "Wizard should initialize with at least one warranty line.")
        wizard.warranty_line_ids.write({'warranty_id': self.warranty_config.id})
        wizard.action_confirm()
        warranty_lines = self.env['sale.order.line'].search([
            ('order_id', '=', self.sale_order.id),
            ('linked_line_id', '=', self.sale_order_line_warranty.id)
        ])
        self.assertTrue(warranty_lines, "A warranty line should be created when a configuration is selected.")
        self.assertEqual(warranty_lines.product_id, self.warranty_config.product_id.product_variant_id, "The warranty product should match the configuration.")
        self.assertEqual(warranty_lines.price_unit, self.sale_order_line_warranty.price_unit * (self.warranty_config.percentage / 100), "The warranty price should be correctly calculated.")

    def test_no_warranty_added_when_not_selected(self):
        # Test that no warranty line is added if no warranty configuration is selected
        self.sale_order.write({'order_line': [
            (1, self.sale_order_line_non_warranty.id, {'product_id': self.product_non_warranty.product_variant_id.id}),
            (1, self.sale_order_line_warranty.id, {'product_id': self.product_warranty.product_variant_id.id}),
        ]})
        wizard = self.env['product.add.warranty'].with_context(active_id=self.sale_order.id).create({})
        wizard.action_confirm()
        warranty_lines = self.env['sale.order.line'].search([('order_id', '=', self.sale_order.id), ('linked_line_id', '=', self.sale_order_line_warranty.id)])
        self.assertFalse(warranty_lines, "No warranty line should be created without configuration")
