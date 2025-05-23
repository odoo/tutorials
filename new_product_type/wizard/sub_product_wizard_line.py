# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SubProductWizardLine(models.TransientModel):
    _name = 'sub.product.wizard.line'

    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    quantity = fields.Float(string="Quantity")
    price = fields.Float(string="Price")
    sale_order_line_id = fields.Many2one(comodel_name="sale.order.line")
    sub_product_wizard_id = fields.Many2one(comodel_name="sub.product.wizard")
