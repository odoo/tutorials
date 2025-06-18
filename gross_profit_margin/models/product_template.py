from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    gross_profit_margin = fields.Float(
        compute='_gross_profit_margin',
        inverse="_inverse_gross_profit_margin",
        string='Gross Profit Margin',
        help='Gross Profit Margin for this product',
    )

    @api.depends('list_price', 'standard_price')
    def _gross_profit_margin(self):
        for product in self:
            if product.list_price:
                if product.standard_price != 0:
                    product.gross_profit_margin = (product.list_price - product.standard_price) / product.standard_price
                else:
                    product.gross_profit_margin = 0.0
            else:
                product.gross_profit_margin = 0.0

    def _inverse_gross_profit_margin(self):
        for product in self:
            if product.gross_profit_margin:
                product.list_price = (product.standard_price * product.gross_profit_margin) + product.standard_price
