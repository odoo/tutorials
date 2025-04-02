# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class WarrantyConfiguration(models.Model):
    _name = 'warranty.configuration'
    _description = "Warranty Configuration"

    name = fields.Char(string="Name")
    product_id = fields.Many2one(comodel_name='product.product', string="Product",  required=True)
    percentage = fields.Float(string="Percentage")
    validity = fields.Integer(string="Valid For(Years)", required=True)
