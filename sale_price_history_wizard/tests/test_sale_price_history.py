# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestSalePriceHistoryWizard(TransactionCase):

    def setUp(self):
        super().setUp()
        self.product = self.env['product.product'].create({'name': 'Test Product'})
        self.partner = self.env['res.partner'].create({'name': 'Test Customer'})
        self.sale_order = self.env['sale.order'].create({'partner_id': self.partner.id})
        self.order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'price_unit': 100.0,
        })
        self.wizard = self.env['sale.price.history.wizard'].with_context(
            default_product_id=self.product.id,
            default_partner_id=self.partner.id,
        ).create({})

    def test_default_get(self):
        """Test that the wizard correctly fetches default values from context"""
        self.assertEqual(self.wizard.product_id, self.product)
        self.assertEqual(self.wizard.partner_id, self.partner)

    def test_wizard_action(self):
        """Test that the wizard action opens the correct form"""
        action = self.wizard.with_context(active_id=self.order_line.id).default_get([])
        self.assertIn('partner_id', action)

    def test_show_price_history_button(self):
        """Test that clicking the button opens the sales price history wizard"""
        action = self.env.ref('sale_price_history_wizard.action_sale_price_history').read()[0]
        self.assertEqual(action['res_model'], 'sale.price.history.wizard')
        self.assertEqual(action['view_mode'], 'form')
        self.assertEqual(action['target'], 'new')
