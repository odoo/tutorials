from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestAddWarranty(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({'name': 'Test Customer'})
        self.sale_order = self.env['sale.order'].create({'name': 'Test SO', 'partner_id': self.partner.id })
        
        self.product_with_warranty = self.env['product.template'].create({
            'name': 'Product with Warranty',
            'is_warranty_available': True
        })
        
        self.product_without_warranty = self.env['product.template'].create({
            'name': 'Product without Warranty',
            'is_warranty_available': False
        })
        
        self.so_line_with_warranty = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_with_warranty.product_variant_id.id,
            'name': 'Line with Warranty'
        })
        
        self.so_line_without_warranty = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_without_warranty.product_variant_id.id,
            'name': 'Line without Warranty'
        })
    
    def test_wizard_default_get(self):
        """Tests the correct initialization of the wizard"""
        wizard = self.env['add.product.warranty'].with_context(active_id=self.sale_order.id).create({})
        
        self.assertEqual(wizard.sale_order_id.id, self.sale_order.id, "Wizard should be linked with correct sale order ID")
        self.assertIn(self.so_line_with_warranty, wizard.warranty_line_ids.mapped("sale_order_line_id"), "Warranty enabled products must be in wizard warranty lines")
        self.assertNotIn(self.so_line_without_warranty, wizard.warranty_line_ids.mapped("sale_order_line_id"), "Product with warranty not enabled must not be in wizard warranty line")

    def test_action_add_warranty(self):
        """Test if the warranty is correctly added to the sale order when a valid configuration is selected"""
        wizard = self.env['add.product.warranty'].with_context(active_id=self.sale_order.id).create({})
        warranty_prod = self.env["product.template"].create({ 'name': 'Warranty 1 Year', 'type': 'service' })
        warranty_configuration_one_year = self.env['product.warranty.configuration'].create({
            'name': 'Extended Warranty One Year',
            'product_id': warranty_prod.id,
            'percentage': 10.0,
            'duration': 1
        })
        self.env['product.warranty.line'].create({
            'wizard_id': wizard.id,
            'warranty_configuration_id': warranty_configuration_one_year.id,
            'sale_order_line_id': self.so_line_with_warranty.id
        })
        
        wizard.action_add_warranty()
        warranty_line = self.sale_order.order_line.filtered(
            lambda line: line.product_id == warranty_configuration_one_year.product_id.product_variant_id
        )

        self.assertTrue(warranty_line, "Warranty line must be added to the sale order")

    def test_no_warranty_added_without_configuration(self):
        """Tests that no warranty is added if no warranty configuration is selected"""
        wizard = self.env['add.product.warranty'].with_context(active_id=self.sale_order.id).create({})
        self.env['product.warranty.line'].create({
            'wizard_id': wizard.id,
            'sale_order_line_id': self.so_line_with_warranty.id
        })
        
        existing_lines = self.sale_order.order_line.sorted('id').mapped('id')
        wizard.action_add_warranty()
        new_lines = self.sale_order.order_line.sorted('id').mapped('id')
        self.assertListEqual(existing_lines, new_lines, "No new sale order line should be added when no warranty configuration is selected")
