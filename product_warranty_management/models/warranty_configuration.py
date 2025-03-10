# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class WarrantyConfiguration(models.Model):
    _name = 'warranty.configuration'
    _description = 'Warranty Configuration'
    _rec_name = 'validity'

    name = fields.Char(string="Name")
    validity = fields.Integer(string="Valid For(Years)", required=True, default=1)
    product_id = fields.Many2one(comodel_name='product.product', string="Product", required=True)
    percentage = fields.Float(string="Percentage", required=True)

    _sql_constraints = [
        ('check_positive_validity', 'check(validity > 0)', "Waranty Duration Value must be positive"),
        ('check_percentage', 'check(percentage > 0)', "Waranty percentage must be positive")
    ]
