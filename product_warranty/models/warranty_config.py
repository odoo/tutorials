from odoo import models, fields

class WarrantyConfig(models.Model):
    _name = 'warranty.config'
    _description = 'Warranty Configuration'

    name = fields.Char(string="Name")
    product = fields.Many2one('product.product', string="Warranty Product")
    period = fields.Float(string='Period (in years)', default=1)
    percentage = fields.Float(string="Percentage (%)")
