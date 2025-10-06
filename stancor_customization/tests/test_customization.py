# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestStancorCustomization(TransactionCase):
    def setUp(self):
        super().setUp()
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'wt_per_mt': 10.0,
            'wt_per_pc': 2.0,
            'type': 'consu',  
            'invoice_policy': 'order',
        })
        self.sale_order = self.env['sale.order'].create({'partner_id': self.env.ref('base.res_partner_1').id})
        self.sale_order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 100,
            's_quantity': 10,
            's_unit': 'mtrs',
        })
        
    def test_sale_order_line_onchange(self):
        self.sale_order_line._onchange_s_unit()
        if self.sale_order_line.product_uom_qty != 100:
            raise ValidationError("UOM quantity mismatch: Expected 100, got %s" % self.sale_order_line.product_uom_qty)
        
    def test_mrp_production_compute_s_quantity(self):
        mrp_production = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'product_qty': 100,
            's_unit': 'mtrs',
        })
        mrp_production._compute_s_quantity()
        if mrp_production.s_quantity != 10:
            raise ValidationError("MRP S.Quantity computation is incorrect: Expected 10, got %s" % mrp_production.s_quantity)
        
    def test_stock_move_compute_s_quantity(self):
        stock_move = self.env['stock.move'].create({
            'name': 'Test Move',
            'product_id': self.product.id,
            'quantity': 100,
            'sale_line_id': self.sale_order_line.id,
            's_unit': 'pcs',
            'product_uom': self.product.uom_id.id,  
            'product_uom_qty': 100.0, 
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
        })
        stock_move.s_unit = 'pcs' 
        stock_move._compute_s_quantity()
        if stock_move.s_quantity != 50:
            raise ValidationError(f"Stock Move S.Quantity computation is incorrect: Expected 50, got {stock_move.s_quantity}")
 
    def test_invoice_line_quantity(self):
        invoice_line_vals = self.sale_order_line._prepare_invoice_line()
        if invoice_line_vals['quantity'] != self.sale_order_line.s_quantity:
            raise ValidationError("Invoice Line Quantity mismatch: Expected %s, got %s" % (self.sale_order_line.s_quantity, invoice_line_vals['quantity']))
