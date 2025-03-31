# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    gross_profit_margin = fields.Float(compute='_compute_gross_profit_margin', inverse='_inverse_gross_profit_margin', readonly=False)
    
    @api.depends('list_price', 'standard_price')
    def _compute_gross_profit_margin(self):
        for product in self:
            if not product.list_price:
                product.gross_profit_margin = 0.0
            else:
                product.gross_profit_margin = ((product.list_price - product.standard_price) / product.list_price) * 100
                
    def _inverse_gross_profit_margin(self):
        for product in self:
            if product.gross_profit_margin is None:
                product.list_price = product.standard_price   
            elif product.gross_profit_margin <= -100:
                raise UserError(_("Margin cannot be -100% or lower. Please enter a valid percentage."))
            elif product.gross_profit_margin >= 100:
                raise UserError(_("Margin cannot be 100% or higher. Please enter a valid percentage."))
            else:
                product.list_price = product.standard_price / (1 - (product.gross_profit_margin / 100))
