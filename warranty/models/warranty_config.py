from odoo import fields, models


class WarrantyConfiguration(models.Model):
    _name = 'warranty.config'
    _description = 'Warranty Configuration'

    name = fields.Char(string='Warranty Name', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    percentage = fields.Float(string='Percentage (%)', required=True)
    years = fields.Integer(string='Years', required=True)
