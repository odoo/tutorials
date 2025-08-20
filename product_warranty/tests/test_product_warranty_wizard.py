# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestProductWarrantyWizard(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer'
        })
        ProductTemplate = self.env['product.template']
        warranty_template = ProductTemplate.create({
            'name': 'Warranty Product',
            'warranty': True,
        })
        no_warranty_template = ProductTemplate.create({
            'name': 'Non-Warranty Product',
            'warranty': False,
        })
        self.warranty_product = warranty_template.product_variant_id
        self.no_warranty_product = no_warranty_template.product_variant_id

        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })
        self.sol_with_warranty = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.warranty_product.id,
            'product_uom_qty': 1,
            'price_unit': 100,
        })
        self.sol_without_warranty = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.no_warranty_product.id,
            'product_uom_qty': 1,
            'price_unit': 100,
        })

    def test_default_get_populates_wizard_lines(self):
        """Wizard should only include products with warranty=True"""

        wizard = self.env['product.warranty.wizard'].with_context(
            default_sale_order_id=self.sale_order.id
        ).new({})

        wizard.default_get(['wizard_line_ids'])
        self.assertEqual(len(wizard.wizard_line_ids), 1)

        wizard_line = wizard.wizard_line_ids[0]
        self.assertEqual(wizard_line.product_id.id, self.warranty_product.id)
        self.assertEqual(wizard_line.sale_order_line_id.id, self.sol_with_warranty.id)

    def test_action_add_warranty_raises_if_config_missing(self):
        """Should raise UserError if any wizard line has no warranty_config_id"""

        wizard = self.env['product.warranty.wizard'].with_context(
            default_sale_order_id=self.sale_order.id
        ).create({})

        with self.assertRaises(UserError):
            wizard.action_add_warranty()
